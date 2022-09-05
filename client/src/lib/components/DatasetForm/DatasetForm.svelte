<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type {
    DataFormat,
    DatasetFormData,
    UpdateFrequency,
  } from "src/definitions/datasets";
  import type { Tag } from "src/definitions/tag";
  import { DATA_FORMAT_LABELS, UPDATE_FREQUENCY_LABELS } from "src/constants";
  import { formatHTMLDate } from "$lib/util/format";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { user } from "src/lib/stores/auth";
  import ContactEmailsField from "../ContactEmailsField/ContactEmailsField.svelte";
  import GeographicalCoverageField from "./_GeographicalCoverageField.svelte";
  import Select from "../Select/Select.svelte";
  import InputField from "../InputField/InputField.svelte";
  import TextareaField from "../TextareaField/TextareaField.svelte";
  import { toSelectOptions } from "src/lib/transformers/form";
  import { handleSelectChange } from "src/lib/util/form";
  import { Maybe } from "$lib/util/maybe";
  import TagSelector from "../TagSelector/TagSelector.svelte";
  import LicenseField from "./_LicenseField.svelte";

  export let submitLabel = "Publier la fiche de données";
  export let loadingLabel = "Publication en cours...";
  export let loading = false;
  export let tags: Tag[] = [];
  export let licenses: string[] = [];
  export let geographicalCoverages: string[] = [];

  export let initial: DatasetFormData | null = null;

  const dispatch =
    createEventDispatcher<{ save: DatasetFormData; touched: boolean }>();

  type DatasetFormValues = {
    title: string;
    description: string;
    service: string;
    dataFormats: boolean[];
    producerEmail: string | null;
    contactEmails: string[];
    geographicalCoverage: string;
    lastUpdatedAt: string | null;
    updateFrequency: UpdateFrequency | null;
    technicalSource: string | null;
    url: string | null;
    license: string;
    tags: Tag[];
  };

  const dataFormatChoices = Object.entries(DATA_FORMAT_LABELS).map(
    ([value, label]: [DataFormat, string]) => ({ value, label })
  );

  const initialValues: DatasetFormValues = {
    title: initial?.title || "",
    description: initial?.description || "",
    service: initial?.service || "",
    dataFormats: dataFormatChoices.map(
      ({ value }) => !!(initial?.formats || []).find((v) => v === value)
    ),
    producerEmail: initial?.producerEmail || "",
    contactEmails: initial?.contactEmails || [$user?.email || ""],
    lastUpdatedAt: initial?.lastUpdatedAt
      ? formatHTMLDate(initial.lastUpdatedAt)
      : null,
    geographicalCoverage: initial?.geographicalCoverage || "",
    updateFrequency: initial?.updateFrequency || null,
    technicalSource: initial?.technicalSource || null,
    url: initial?.url || null,
    license: initial?.license || "",
    tags: initial?.tags || [],
  };

  // Handle this value manually.
  const dataFormatsValue = initialValues.dataFormats;

  const { form, errors, handleChange, handleSubmit, updateValidateField } =
    createForm({
      initialValues,
      validationSchema: yup.object().shape({
        title: yup.string().required("Ce champ est requis"),
        description: yup.string().required("Ce champs est requis"),
        service: yup.string().required("Ce champs est requis"),
        dataFormats: yup.array(yup.boolean()).length(dataFormatsValue.length),
        producerEmail: yup
          .string()
          .email("Ce champ doit contenir une adresse e-mail valide")
          .nullable(),
        contactEmails: yup
          .array()
          .of(
            yup
              .string()
              .email("Ce champ doit contenir une adresse e-mail valide")
          )
          .min(1),
        lastUpdatedAt: yup.date().nullable(),
        updateFrequency: yup.string().nullable(),
        geographicalCoverage: yup.string().required("Ce champs est requis"),
        technicalSource: yup.string().nullable(),
        url: yup.string().nullable(),
        license: yup.string().nullable(),
        tags: yup
          .array()
          .of(
            yup.object().shape({
              name: yup.string(),
              id: yup.string(),
            })
          )
          .min(1, "Veuillez séléctionner au moins 1 mot-clé"),
      }),
      onSubmit: (values: DatasetFormValues) => {
        const formats = values.dataFormats
          .map((checked, index) =>
            checked ? dataFormatChoices[index].value : null
          )
          .filter(Maybe.Some);

        // Ensure "" becomes null.
        const producerEmail = values.producerEmail
          ? values.producerEmail
          : null;

        const contactEmails = values.contactEmails.filter(Boolean);

        const lastUpdatedAt = values.lastUpdatedAt
          ? new Date(values.lastUpdatedAt)
          : null;

        // Ensure "" becomes null.
        const url = values.url ? values.url : null;
        const license = values.license ? values.license : null;

        const data: DatasetFormData = {
          ...values,
          formats,
          producerEmail,
          contactEmails,
          lastUpdatedAt,
          url,
          license,
        };

        dispatch("save", data);
      },
    });

  $: saveBtnLabel = loading ? loadingLabel : submitLabel;

  $: emailErrors = $errors.contactEmails as unknown as string[];

  export const submitForm = (event: Event) => {
    handleSubmit(event);
  };

  const handleFieldChange = async (event: Event) => {
    dispatch("touched", true);
    handleChange(event);
  };

  const hasError = (error: string | string[]) => {
    return typeof error === "string" && Boolean(error);
  };

  const handleDataformatChange = (event: Event, index: number) => {
    const { checked } = event.target as HTMLInputElement;
    dataFormatsValue[index] = checked;
    updateValidateField("dataFormats", dataFormatsValue);
    dispatch("touched");
  };

  const handleContactEmailsChange = () => {
    // Skip regular handleChange() as the array has already been updated.
    dispatch("touched");
  };

  const handleLastUpdatedAtChange = async (
    event: Event & { currentTarget: EventTarget & HTMLInputElement }
  ) => {
    if (!event.currentTarget.value /* Empty date */) {
      // Needs manual handling, otherwise yup would call e.g. new Date("") which is invalid.
      updateValidateField("lastUpdatedAt", null);
      dispatch("touched");
    } else {
      await handleFieldChange(event);
    }
  };

  const handleTagsChange = async (event: CustomEvent<Tag[]>) => {
    updateValidateField("tags", event.detail);
    dispatch("touched");
  };
</script>

<form
  on:submit={submitForm}
  data-bitwarden-watching="1"
  aria-label="Informations sur le jeu de données"
>
  <h2 id="information-generales" class="fr-mb-5w">Informations générales</h2>

  <div class="form--content fr-mb-8w">
    <InputField
      name="title"
      label="Nom du jeu de données"
      hintText="Ce nom doit aller à l'essentiel et permettre d'indiquer en quelques mots les informations que l'on peut y trouver. Pour des raisons pratiques il est limité à 100 caractères."
      required
      value={$form.title}
      error={$errors.title}
      on:input={handleFieldChange}
      on:blur={handleFieldChange}
    />

    <TextareaField
      name="description"
      label="Description du jeu de données"
      hintText="Quel type de données sont contenues dans ce jeu de données ? Les informations saisies ici seront utilisées par le moteur de recherche."
      required
      value={$form.description}
      error={$errors.description}
      on:input={handleFieldChange}
      on:blur={handleFieldChange}
    />

    <InputField
      name="service"
      label="Service producteur"
      hintText="Service producteur du jeu de données au sein de l'organisation."
      required
      value={$form.service}
      error={$errors.service}
      on:input={handleFieldChange}
      on:blur={handleFieldChange}
    />

    <GeographicalCoverageField
      value={$form.geographicalCoverage}
      error={$errors.geographicalCoverage}
      suggestions={geographicalCoverages}
      on:input={(ev) => updateValidateField("geographicalCoverage", ev.detail)}
    />
  </div>

  <h2 id="source-formats" class="fr-mt-6w fr-mb-5w">Sources et formats</h2>

  <div class="form--content fr-mb-8w">
    <fieldset
      class="fr-fieldset fr-mb-4w {hasError($errors.dataFormats)
        ? 'fr-fieldset--error'
        : ''}"
      aria-describedby={hasError($errors.dataFormats)
        ? "dataformats-desc-error"
        : null}
      role="group"
    >
      <legend
        class="fr-fieldset__legend fr-text--regular"
        id="dataformats-hint-legend"
      >
        Format(s) des données
        <RequiredMarker />
        <span class="fr-hint-text" id="select-hint-dataformats-hint">
          Sélectionnez ici les différents formats de données qu'un réutilisateur
          potentiel pourrait exploiter.
        </span>
      </legend>
      <div class="fr-fieldset__content">
        {#each dataFormatChoices as { value, label }, index (value)}
          {@const id = `dataformats-${value}`}
          <div class="fr-checkbox-group">
            <input
              type="checkbox"
              {id}
              name="dataformats"
              {value}
              required={dataFormatsValue.every((checked) => !checked)}
              checked={dataFormatsValue[index]}
              on:change={(event) => handleDataformatChange(event, index)}
            />
            <label for={id}>
              {label}
            </label>
          </div>
        {/each}
      </div>
      {#if hasError($errors.dataFormats)}
        <p id="dataformats-desc-error" class="fr-error-text">
          {$errors.dataFormats}
        </p>
      {/if}
    </fieldset>

    <InputField
      name="technicalSource"
      label="Système d'information source"
      hintText="De quelle sources proviennent ces données ? Séparez leur nom par des “/” lorsqu'il y en a plusieurs."
      value={$form.technicalSource}
      error={$errors.technicalSource}
      on:input={handleFieldChange}
      on:blur={handleFieldChange}
    />
  </div>

  <h2 id="mot-cles" class="fr-mb-5w">Mot-clés thématiques</h2>

  <div class="form--content fr-mb-8w">
    <TagSelector
      error={typeof $errors.tags === "string" ? $errors.tags : ""}
      selectedTags={initialValues.tags}
      on:change={handleTagsChange}
      name="tags"
      {tags}
    />
  </div>

  <h2 id="contacts" class="fr-mt-6w fr-mb-5w">Contacts</h2>

  <p class="fr-mb-6w">
    Dans un soucis de traçabilité et de facilité de mise à jour, il est
    fondamental de pouvoir prendre contact avec l'organisation ou les personnes
    productrices d'une donnée. Lorsqu'une demande de contact sera effectuée,
    l'ensemble des adresses e-mail saisies recevront la notification.
  </p>

  <div class="form--content fr-mb-8w">
    <InputField
      name="producerEmail"
      label=" Adresse e-mail du service producteur"
      hintText="Il est fortement conseillé d'avoir une adresse e-mail générique afin de rendre la prise de contact possible quelle que soit les personnes en responsabilité. Nous recommandons d'avoir une adresse différente pour chaque service afin de ne pas “polluer” les boîtes e-mail de chacun lorsque le catalogue grandit."
      type="email"
      value={$form.producerEmail}
      error={$errors.producerEmail}
      on:input={handleFieldChange}
    />

    <ContactEmailsField
      bind:errors={emailErrors}
      bind:contactEmails={$form.contactEmails}
      on:blur={handleContactEmailsChange}
      on:input={handleContactEmailsChange}
    />
  </div>

  <h2 id="mise-a-jour" class="fr-mt-6w fr-mb-5w">Mise à jour</h2>

  <p class="fr-mb-5w">
    A moins qu'il ne soit une production ponctuelle, un jeu de données n'est
    utile que lorsqu'il est à jour ! Avec ces quelques informations nous
    pourrons indiquer à vos réutilisateurs lorsque les données seront mises à
    jour.
  </p>

  <div class="form--content fr-mb-8w">
    <InputField
      name="lastUpdatedAt"
      label="Date de la dernière mise à jour (JJ / MM / AAAA)"
      type="date"
      value={$form.lastUpdatedAt}
      error={$errors.lastUpdatedAt}
      on:input={handleLastUpdatedAtChange}
    />

    <Select
      options={toSelectOptions(UPDATE_FREQUENCY_LABELS)}
      id="updateFrequency"
      name="updateFrequency"
      placeholder="Sélectionner une option"
      label="Fréquence de mise à jour"
      value={$form.updateFrequency}
      on:change={(event) =>
        handleSelectChange(
          "updateFrequency",
          event,
          handleFieldChange,
          updateValidateField
        )}
      on:blur={(event) =>
        handleSelectChange(
          "updateFrequency",
          event,
          handleFieldChange,
          updateValidateField
        )}
      error={$errors.updateFrequency}
    />
  </div>

  <h2 id="acces-aux-donnees" class="fr-mt-6w fr-mb-5w">Accès aux données</h2>

  <div class="form--content fr-mb-8w">
    <InputField
      name="url"
      label="Lien vers les données"
      hintText="Saisissez ici le lien de la page web associée au jeu de données."
      value={$form.url}
      error={$errors.url}
      on:input={handleFieldChange}
      on:blur={handleFieldChange}
    />

    <LicenseField
      value={$form.license}
      error={$errors.license}
      suggestions={licenses}
      on:input={(ev) => updateValidateField("license", ev.detail)}
    />
  </div>

  <div class="fr-input-group button--container fr-mb-6w">
    <button
      type="submit"
      class="fr-btn  fr-icon-upload-2-line fr-btn--icon-right"
    >
      {saveBtnLabel}
    </button>
  </div>
</form>

<style>
  h2 {
    /* Prevent h2 to be covered by the header
    See https://css-tricks.com/fixed-headers-and-jump-links-the-solution-is-scroll-margin-top/
    
    */
    scroll-margin-top: 10vh;
  }

  .button--container {
    display: flex;
    justify-content: flex-end;
  }

  .form--content {
    width: 80%;
    padding: auto;
    margin: auto;
  }
</style>
