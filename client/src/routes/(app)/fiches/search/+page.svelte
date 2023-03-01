<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFiltersValue } from "src/definitions/datasetFilters";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import FilterPanel from "./_FilterPanel.svelte";
  import PaginationContainer from "$lib/components/PaginationContainer/PaginationContainer.svelte";
  import {
    toFiltersParams,
    toFiltersValue,
  } from "src/lib/transformers/datasetFilters";
  import { makePageParam } from "$lib/util/pagination";
  import { page as pageStore } from "$app/stores";
  import type { PageData } from "./$types";
  import { onMount } from "svelte";

  export let data: PageData;

  $: ({ paginatedDatasets, q, currentPage, filtersInfo, filtersValue } = data);

  let displayFilters = false;

  onMount(() => {
    const searchParams = $pageStore.url.searchParams;
    const filtersParams = toFiltersValue(searchParams);
    displayFilters = Object.values(filtersParams).some((val) => val != null);
  });

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
      <div class="fr-col-12 fr-pb-1w summary__header">
        <h2>
          {paginatedDatasets.totalItems}
          {pluralize(
            paginatedDatasets.totalItems,
            "fiche de données",
            "fiches de données"
          )}
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
      <FilterPanel
        on:change={handleFilterChange}
        info={filtersInfo}
        value={filtersValue}
      />
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

  .summary__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
