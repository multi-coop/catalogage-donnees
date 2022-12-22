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
  import SkipLink from "src/lib/components/SkipLink/SkipLink.svelte";

  let modalControlId = "confirm-stop-contributing-modal";

  let loading = false;

  let formHasBeenTouched = false;

  export let data: PageData;

  $: ({ catalog, tags, licenses, filtersInfo } = data);

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      const tagIds = event.detail.tags.map((item) => item.id);
      const dataset = await createDataset({
        fetch,
        apiToken: $apiTokenStore,
        data: { tagIds, ...event.detail },
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
</script>

<SkipLink linksMap={{ formulaire: "main" }} />

<!-- svelte-ignore a11y-no-redundant-roles -- this is the page's main header so this role is not rudundant -->
<header role="banner" class="fr-p-4w">
  <div class="fr-col">
    <h1 class="fr-grid-row  fr-h5 fr-text--regular">
      Contribuer une fiche de jeu de données
    </h1>
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
    <!-- We go back to page top if the main container gets focus -->
    <main on:focus={() => window.scroll(0, 0)} tabindex="-1" id="main">
      <DatasetForm
        {catalog}
        {tags}
        {licenses}
        geographicalCoverages={filtersInfo.geographicalCoverage}
        {loading}
        on:save={onSave}
        on:touched={() => (formHasBeenTouched = true)}
      />
    </main>
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
