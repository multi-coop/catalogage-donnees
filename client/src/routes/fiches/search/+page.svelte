<script context="module" lang="ts">
  throw new Error("@migration task: Check code was safely removed (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292722)");

  // import type { Load } from "@sveltejs/kit";
  // import { get } from "svelte/store";
  // import { getDatasets } from "$lib/repositories/datasets";
  // import { apiToken } from "$lib/stores/auth";
  // import { getPageFromParams } from "$lib/util/pagination";
  // import { page as pageStore } from "$app/stores";
  // import { getDatasetFiltersInfo } from "src/lib/repositories/datasetFilters";
  // import { toFiltersValue } from "src/lib/transformers/datasetFilters";

  // export const load: Load = async ({ fetch, url }) => {
  //   const page = getPageFromParams(url.searchParams);
  //   const q = url.searchParams.get("q") || "";
  //   const filtersValue = toFiltersValue(url.searchParams);

  //   const token = get(apiToken);

  //   const [paginatedDatasets, filtersInfo] = await Promise.all([
  //     getDatasets({
  //       fetch,
  //       apiToken: token,
  //       page,
  //       q,
  //       filters: filtersValue,
  //     }),
  //     getDatasetFiltersInfo({ fetch, apiToken: token }),
  //   ]);

  //   return {
  //     props: {
  //       paginatedDatasets,
  //       filtersInfo,
  //       filtersValue,
  //       currentPage: page,
  //       q,
  //     },
  //   };
  // };
</script>

<script lang="ts">
  throw new Error("@migration task: Add data prop (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292707)");

  import { goto } from "$app/navigation";
  import type { Dataset } from "src/definitions/datasets";
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import type { Paginated } from "src/definitions/pagination";
  import FilterPanel from "../_FilterPanel.svelte";
  import { toFiltersParams } from "src/lib/transformers/datasetFilters";
  import { makePageParam } from "$lib/util/pagination";
  import PaginationContainer from "../_PaginationContainer.svelte";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let q: string;
  export let currentPage: number;

  export let filtersInfo: Maybe<DatasetFiltersInfo>;
  export let filtersValue: DatasetFiltersValue;

  let displayFilters = false;

  const updateSearch = async (event: CustomEvent<string>) => {
    const href = patchQueryString($pageStore.url.searchParams, [
      ["q", event.detail || null],
      // If on page n = (2, ...), go back to page 1 on new search.
      makePageParam(1),
    ]);
    goto(href, { noscroll: true });
  };

  const handleFilterChange = async (e: CustomEvent<DatasetFiltersValue>) => {
    const href = patchQueryString($pageStore.url.searchParams, [
      ...toFiltersParams(e.detail),
      makePageParam(1),
    ]);
    goto(href, { noscroll: true });
  };
</script>

<svelte:head>
  <title>Rechercher un jeu de données</title>
</svelte:head>
<section class="fr-background-alt--grey fr-mb-6w">
  <div class="fr-container fr-grid-row fr-grid-row--center fr-py-6w">
    <div class="fr-col-10">
      <h1>Recherchez un jeu de données</h1>
      <SearchForm value={q} on:submit={updateSearch} />
    </div>
  </div>
</section>

<section class="fr-container">
  {#if Maybe.Some(paginatedDatasets)}
    <div class="fr-grid-row summary">
      <div class="fr-col-12 fr-pb-3w summary__header">
        <h2>
          {paginatedDatasets.totalItems}
          {pluralize(paginatedDatasets.totalItems, "résultat", "résultats")}
        </h2>

        <button
          on:click={() => (displayFilters = !displayFilters)}
          class="fr-btn fr-btn--secondary fr-btn--icon-right"
          class:fr-icon-arrow-down-s-line={!displayFilters}
          class:fr-icon-arrow-up-s-line={displayFilters}
        >
          Affiner la recherche
        </button>
      </div>
    </div>

    {#if Maybe.Some(filtersInfo) && displayFilters}
      <div
        data-test-id="filter-panel"
        class="fr-grid-row fr-grid-row--gutters fr-py-3w filters"
      >
        <FilterPanel
          on:change={handleFilterChange}
          info={filtersInfo}
          value={filtersValue}
        />
      </div>
    {/if}

    <div class="fr-grid-row">
      <div class="fr-col-12">
        <DatasetList datasets={paginatedDatasets.items} />

        <PaginationContainer
          {currentPage}
          totalPages={paginatedDatasets.totalPages}
        />
      </div>
    </div>
  {/if}
</section>

<style>
  .summary__header {
    border-bottom: 1px solid var(--border-default-grey);
  }

  h2 {
    padding: 0;
  }

  .filters {
    border-bottom: 1px solid var(--border-default-grey);
    justify-content: space-between;
  }

  .summary__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
