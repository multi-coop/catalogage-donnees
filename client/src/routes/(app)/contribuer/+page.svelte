<script lang="ts">
  import { goto } from "$app/navigation";
  import type { PageData } from "./$types";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import { apiToken as apiTokenStore } from "$lib/stores/auth";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";
  import ModalExitFormConfirmation from "src/lib/components/ModalExitFormConfirmation/ModalExitFormConfirmation.svelte";
  import { hasHistory } from "src/lib/util/history";
  import {
    getDataFormats,
    postDataFormat,
  } from "src/lib/repositories/dataformat";

  let modalControlId = "confirm-stop-contributing-modal";

  let loading = false;

  let formHasBeenTouched = false;

  export let data: PageData;

  $: ({ catalog, tags, licenses, filtersInfo, formats } = data);

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      const tagIds = event.detail.tags.map((item) => item.id);
      const formatIds = event.detail.formats.map((item) => item.id);
      const dataset = await createDataset({
        fetch,
        apiToken: $apiTokenStore,
        data: { ...event.detail, tagIds, formatIds },
      });

      if (Maybe.Some(dataset)) {
        await goto(paths.datasetDetail({ id: dataset.id }));
      }
    } finally {
      loading = false;
    }
  };

  const handleExitForm = async () => {
    if (hasHistory()) {
      history.back();
    } else {
      await goto(paths.home);
    }
  };

  const handleAddFormat = async (e: CustomEvent<string>) => {
    await postDataFormat({ fetch, apiToken: $apiTokenStore, value: e.detail });
    formats = await getDataFormats({ fetch, apiToken: $apiTokenStore });
  };
</script>

<header class="fr-p-4w">
  <div class="fr-col">
    <h5 class="fr-grid-row fr-text--regular">
      Contribuer une fiche de jeu de données
    </h5>
    {#if Maybe.Some(catalog)}
      <p class="fr-grid-row fr-text--sm fr-text-mention--grey">
        Catalogue : {catalog.organization.name}
      </p>
    {/if}
  </div>

  {#if formHasBeenTouched}
    <button
      class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
      data-fr-opened="false"
      data-testid="exit-contribution-form"
      aria-controls={modalControlId}
    >
      {""}
    </button>
  {:else}
    <button
      data-testid="exit-contribution-form"
      class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
      on:click={handleExitForm}
    >
      {""}
    </button>
  {/if}
</header>

{#if Maybe.Some(catalog) && Maybe.Some(tags) && Maybe.Some(licenses) && Maybe.Some(filtersInfo)}
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
      {loading}
      on:save={onSave}
      on:touched={() => (formHasBeenTouched = true)}
      on:addItem={handleAddFormat}
    />
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
