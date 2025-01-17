<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import paths from "$lib/paths";
  import { isAdmin, apiToken } from "$lib/stores/auth";
  import { deleteDataset, updateDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";
  import ModalExitFormConfirmation from "src/lib/components/ModalExitFormConfirmation/ModalExitFormConfirmation.svelte";
  import type { PageData } from "./$types";
  import {
    getDataFormats,
    postDataFormat,
  } from "src/lib/repositories/dataformat";
  import type { DataFormat } from "src/definitions/dataformat";

  export let data: PageData;

  $: ({ catalog, tags, licenses, filtersInfo, formats, dataset } = data);

  let modalControlId = "stop-editing-form-modal";

  let loading = false;

  let formHasbeenTouched = false;

  let freshDataFormat: DataFormat[] = [];

  const handleCreateDataFormat = async (e: CustomEvent<string>) => {
    const dataFormat = await postDataFormat({
      fetch,
      apiToken: $apiToken,
      value: e.detail,
    });

    freshDataFormat = [...freshDataFormat, dataFormat];

    formats = await getDataFormats({ fetch, apiToken: $apiToken });
  };

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    if (!Maybe.Some(dataset)) {
      return;
    }

    const tagIds = event.detail.tags.map((item) => item.id);
    const mergedDataFormatsIds = event.detail.formats.reduce((prev, next) => {
      if (!next.name) {
        return prev;
      }

      if (!next.id) {
        const foundItemId = freshDataFormat.find(
          (item) => item.name === next.name
        )?.id;

        if (!foundItemId) {
          return prev;
        }

        return [...prev, foundItemId];
      }

      return [...prev, next.id];
    }, [] as number[]);

    try {
      loading = true;

      const updatedDataset = await updateDataset({
        fetch,
        apiToken: $apiToken,
        id: dataset.id,
        data: { ...event.detail, tagIds, formatIds: mergedDataFormatsIds },
      });

      if (Maybe.Some(updatedDataset)) {
        await goto(paths.datasetDetail({ id: updatedDataset.id }));
      }
    } finally {
      loading = false;
    }
  };

  const onClickDelete = async (): Promise<void> => {
    if (!Maybe.Some(dataset)) {
      return;
    }

    const confirmed = confirm(
      "Voulez-vous vraiment supprimer ce jeu de données ? Cette opération est irréversible."
    );

    if (!confirmed) {
      return;
    }

    await deleteDataset({ fetch, apiToken: $apiToken, id: dataset.id });
    await goto(paths.home);
  };

  const handleExitForm = async () => {
    if (!Maybe.Some(dataset)) {
      return;
    }
    await goto(paths.datasetDetail({ id: dataset.id }));
  };
</script>

{#if Maybe.Some(catalog) && Maybe.Some(dataset) && Maybe.Some(tags) && Maybe.Some(licenses) && Maybe.Some(filtersInfo) && formats}
  <header class="fr-p-4w">
    <div class="fr-col">
      <h5 class="fr-grid-row fr-text--regular">
        Modifier la fiche de jeu de données
      </h5>
      <p class="fr-grid-row fr-text--sm fr-text-mention--grey">
        Catalogue : {dataset.catalogRecord.organization.name}
      </p>
    </div>
    {#if formHasbeenTouched}
      <button
        class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
        data-fr-opened="false"
        data-testid="exit-edit-form"
        aria-controls={modalControlId}
      >
        {""}
      </button>
    {:else}
      <button
        data-testid="exit-edit-form"
        class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
        on:click={handleExitForm}
      >
        {""}
      </button>
    {/if}
  </header>

  <ModalExitFormConfirmation
    on:confirm={handleExitForm}
    controlId={modalControlId}
  />

  <DatasetFormLayout>
    <DatasetForm
      {formats}
      {catalog}
      {tags}
      {licenses}
      geographicalCoverages={filtersInfo.geographicalCoverage}
      initial={dataset}
      {loading}
      submitLabel="Enregistrer les modifications"
      loadingLabel="Modification en cours..."
      on:save={onSave}
      on:createDataFormat={handleCreateDataFormat}
      on:touched={() => (formHasbeenTouched = true)}
    />

    {#if $isAdmin}
      <div class="fr-alert fr-alert--error fr-mt-8w">
        <p>
          <strong> Zone de danger </strong>
          <em>(visible car vous avez le rôle admin)</em>
        </p>

        <button
          class="fr-btn fr-btn--secondary"
          on:click|preventDefault={onClickDelete}
        >
          Supprimer ce jeu de données
        </button>
      </div>
    {/if}
  </DatasetFormLayout>
{/if}

<style>
  header {
    height: 12vh;
    display: flex;
    position: sticky;
    justify-content: space-between;
    top: 0;
    z-index: 55;
    background-color: var(--background-default-grey);
  }
</style>
