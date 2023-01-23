<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type {
    DatasetFormData,
    DatasetFormInitial,
    PublicationRestriction,
    UpdateFrequency,
  } from "src/definitions/datasets";
  import type { Tag } from "src/definitions/tag";
  import {
    PUBLICATION_RESTRICTIONS_OPTIONS,
    UPDATE_FREQUENCY_LABELS,
  } from "src/constants";
  import { formatHTMLDate } from "$lib/util/format";
  import { account } from "src/lib/stores/auth";
  import ContactEmailsField from "../ContactEmailsField/ContactEmailsField.svelte";
  import GeographicalCoverageField from "./_GeographicalCoverageField.svelte";
  import Select from "../Select/Select.svelte";
  import InputField from "../InputField/InputField.svelte";
  import TextareaField from "../TextareaField/TextareaField.svelte";
  import {
    toSelectOptions,
    transformDataFormatToSelectOption,
    transoformSelectOptionToDataFormat,
  } from "src/lib/transformers/form";
  import { handleSelectChange } from "src/lib/util/form";
  import TagSelector from "../TagSelector/TagSelector.svelte";
  import RadioGroupField from "../RadioGroupField/RadioGroupField.svelte";
  import LicenseField from "./_LicenseField.svelte";
  import type { Catalog, ExtraFieldValue } from "src/definitions/catalogs";
  import ExtraField from "./_ExtraField.svelte";
  import Alert from "../Alert/Alert.svelte";
  import type { DataFormat } from "src/definitions/dataformat";
  import FormatSelector from "./_SearcheableComboBox.svelte";
  import type { SelectOption } from "src/definitions/form";
  import SearcheableComboBox from "./_SearcheableComboBox.svelte";

  export let submitLabel = "Publier la fiche de données";
  export let loadingLabel = "Publication en cours...";
  export let loading = false;
  export let catalog: Catalog;
  export let tags: Tag[] = [];
  export let formats: DataFormat[];
  export let licenses: string[] = [];
  export let geographicalCoverages: string[] = [];

  export let initial: DatasetFormInitial | null = null;

  const dispatch =
    createEventDispatcher<{ save: DatasetFormData; touched: boolean }>();

  type DatasetFormValues = {
    organizationSiret: string;
    title: string;
    description: string;
    service: string;
    formats: SelectOption<number>[];
    producerEmail: string | null;
    contactEmails: string[];
    geographicalCoverage: string;
    lastUpdatedAt: string | null;
    updateFrequency: UpdateFrequency | null;
    technicalSource: string | null;
    url: string | null;
    license: string;
    tags: Tag[];
    extraFieldValues: string[];
    publicationRestriction: PublicationRestriction;
  };

  const initialValues: DatasetFormValues = {
    organizationSiret: catalog.organization.siret,
    title: initial?.title || "",
    description: initial?.description || "",
    service: initial?.service || "",
    formats: initial
      ? initial.formats.map(transformDataFormatToSelectOption)
      : [],
    producerEmail: initial?.producerEmail || "",
    contactEmails: initial?.contactEmails || [$account?.email || ""],
    lastUpdatedAt: initial?.lastUpdatedAt
      ? formatHTMLDate(initial.lastUpdatedAt)
      : null,
    geographicalCoverage: initial?.geographicalCoverage || "",
    updateFrequency: initial?.updateFrequency || null,
    technicalSource: initial?.technicalSource || null,
    url: initial?.url || null,
    license: initial?.license || "",
    tags: initial?.tags || [],
    extraFieldValues: catalog.extraFields.map((f) => {
      const fieldValue = (initial?.extraFieldValues || []).find(
        ({ extraFieldId }) => f.id === extraFieldId
      );
      return fieldValue?.value || "";
    }),
    publicationRestriction: initial?.publicationRestriction || "no_restriction",
  };

  const { form, errors, handleChange, handleSubmit, updateValidateField } =
    createForm({
      initialValues,
      validationSchema: yup.object().shape({
        organizationSiret: yup.string().required("Ce champs est requis"),
        publicationRestriction: yup.string().required("Ce champs est requis"),
        title: yup.string().required("Ce champ est requis"),
        description: yup.string().required("Ce champs est requis"),
        service: yup.string().required("Ce champs est requis"),
        formats: yup
          .array()
          .of(
            yup.object().shape({
              label: yup.string(),
              value: yup.number(),
            })
          )
          .min(1, "Veuillez séléctionner au moins 1 mot-clé"),
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
        extraFieldValues: yup.array().of(yup.string()),
      }),
      onSubmit: (values: DatasetFormValues) => {
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

        let extraFieldValues: ExtraFieldValue[] = [];

        values.extraFieldValues.forEach((value, index) => {
          if (value) {
            extraFieldValues.push({
              extraFieldId: catalog.extraFields[index].id,
              value,
            });
          }
        });

        const data: DatasetFormData = {
          ...values,
          formats: values.formats.map(transoformSelectOptionToDataFormat),
          producerEmail,
          contactEmails,
          lastUpdatedAt,
          url,
          license,
          extraFieldValues,
        };
        dispatch("save", data);
      },
    });

  $: saveBtnLabel = loading ? loadingLabel : submitLabel;

  $: emailErrors = $errors.contactEmails as unknown as string[];

  $: console.log($errors.formats);

  export const submitForm = (event: Event) => {
    event.preventDefault();
    handleSubmit(event);
  };

  const handleFieldChange = async (event: Event) => {
    handleChange(event);
    dispatch("touched", true);
  };

  const handleDataFormatChanges = async (
    event: CustomEvent<SelectOption<number>[]>
  ) => {
    updateValidateField("formats", event.detail);
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

  const handleExtraFieldChange = (event: Event, index: number) => {
    const { value } = event.target as HTMLInputElement | HTMLSelectElement;
    const v = $form.extraFieldValues;
    v[index] = value;
    updateValidateField("extraFieldValues", v);
    dispatch("touched");
  };
</script>

<form
  on:submit={submitForm}
  data-bitwarden-watching="1"
  novalidate
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
    />

    <TextareaField
      name="description"
      label="Description du jeu de données"
      hintText="Quel type de données sont contenues dans ce jeu de données ? Les informations saisies ici seront utilisées par le moteur de recherche."
      required
      value={$form.description}
      error={$errors.description}
      on:input={handleFieldChange}
    />

    <InputField
      name="service"
      label="Service producteur"
      hintText="Service producteur du jeu de données au sein de l'organisation."
      required
      value={$form.service}
      error={$errors.service}
      on:input={handleFieldChange}
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
    <SearcheableComboBox
      label={"Format(s) des données"}
      hintText={"Sélectionnez ici les différents formats de données qu'un réutilisateur potentiel pourrait exploiter."}
      name="dataFormats"
      options={formats.map(transformDataFormatToSelectOption)}
      error={typeof $errors.formats === "string" ? $errors.formats : ""}
      on:input={handleDataFormatChanges}
    />
    <InputField
      name="technicalSource"
      label="Système d'information source"
      hintText="De quelle sources proviennent ces données ? Séparez leur nom par des “/” lorsqu'il y en a plusieurs."
      value={$form.technicalSource}
      error={$errors.technicalSource}
      on:input={handleFieldChange}
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
    />

    <LicenseField
      value={$form.license}
      error={$errors.license}
      suggestions={licenses}
      on:input={(ev) => updateValidateField("license", ev.detail)}
    />
  </div>

  {#if catalog.extraFields.length > 0}
    <h2 id="informations-complementaires" class="fr-mt-6w fr-mb-5w">
      Informations complémentaires
    </h2>

    <div class="form--content fr-mb-8w">
      {#each catalog.extraFields as extraField, index (extraField.id)}
        <ExtraField
          {extraField}
          value={$form.extraFieldValues[index]}
          on:input={(ev) => handleExtraFieldChange(ev, index)}
          on:change={(ev) => handleExtraFieldChange(ev, index)}
          on:blur={(ev) => handleExtraFieldChange(ev, index)}
        />
      {/each}
    </div>
  {/if}

  {#if !initial || (catalog.organization.siret === $account?.organizationSiret && initial)}
    <h2 id="visibilité-fiche" class="fr-mt-6w fr-mb-5w">
      Visibilité de cette fiche catalogue
    </h2>

    <Alert title="Qui peut voir cette fiche ?">
      Par défaut, les fiches catalogues publiées sont accessibles au public (<a
        href="https://catalogue.data.gouv.fr/api/docs#/catalogs/export_catalog_catalogs__siret__export_csv_get"
        target="_blank"
        rel="noopener"
        >via API
      </a>).
      <br /> <br />
      <strong>
        Une fiche catalogue contient les informations concernant un jeu de
        données. Il ne s’agit pas de son contenu.
      </strong>
    </Alert>

    <div class="form--content fr-mb-8w fr-mt-5w">
      <RadioGroupField
        name="publicationRestriction"
        label="L’accès aux informations contribuées sur ce formulaire doit-il être restreint ?"
        hintText="Si le contenu que vous avez saisi contient des données sensibles ou à caractère personnel, il vous est possible de faire en sorte que seuls les membres de votre organisation aient accès à cette fiche."
        options={toSelectOptions(PUBLICATION_RESTRICTIONS_OPTIONS)}
        value={$form.publicationRestriction}
        on:change={handleFieldChange}
        on:blur={handleFieldChange}
        displayOptionsInline={false}
      />
    </div>
  {/if}

  <div class="fr-input-group button--container fr-mb-6w">
    <button class="fr-btn  fr-icon-upload-2-line fr-btn--icon-right">
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
