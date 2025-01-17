<script lang="ts">
  import { goto } from "$app/navigation";
  import type { PageData } from "./$types";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import { apiToken } from "$lib/stores/auth";
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
  import type { DataFormat } from "src/definitions/dataformat";

  let modalControlId = "confirm-stop-contributing-modal";

  let loading = false;

  let formHasBeenTouched = false;

  let freshDataFormat: DataFormat[] = [];

  export let data: PageData;

  $: ({ catalog, tags, licenses, filtersInfo, formats } = data);

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
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

      const dataset = await createDataset({
        fetch,
        apiToken: $apiToken,
        data: { ...event.detail, tagIds, formatIds: mergedDataFormatsIds },
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
  const handleCreateDataFormat = async (e: CustomEvent<string>) => {
    const dataformat = await postDataFormat({
      fetch,
      apiToken: $apiToken,
      value: e.detail,
    });

    freshDataFormat = [...freshDataFormat, dataformat];

    formats = await getDataFormats({ fetch, apiToken: $apiToken });
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
      on:createDataFormat={handleCreateDataFormat}
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
