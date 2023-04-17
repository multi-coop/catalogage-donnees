<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFiltersValue } from "src/definitions/datasetFilters";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
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
  import TextSearchFilter from "src/lib/components/SearchFilter/TextSearchFilter.svelte";

  export let data: PageData;

  $: ({ paginatedDatasets, q, currentPage, filtersInfo, filtersValue } = data);

  let displayFilters = false;

  export let catalogButtonText = "";

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

  const handleFilterChange = async (filtersValues: DatasetFiltersValue) => {
    const href = patchQueryString($pageStore.url.searchParams, [
      ...toFiltersParams(filtersValues),
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
    <div class="fr-grid-row fr-pb-2w summary__header">
      <div class="fr-col-7">
        <TextSearchFilter
          higlighted
          label="Catalogue"
          options={filtersInfo.organizationSiret.map(({ name, siret }) => ({
            label: name,
            value: siret,
          }))}
          buttonText={catalogButtonText ?? "Rechercher..."}
          on:selectOption={(e) => {
            if (!e.detail.value) {
              handleFilterChange({
                organizationSiret: null,
                geographicalCoverage: null,
                service: null,
                formatId: null,
                technicalSource: null,
                tagId: null,
                license: null,
                extraFieldValues: null,
              });

              catalogButtonText = "";
              return;
            }

            catalogButtonText = e.detail.label;
            handleFilterChange({
              organizationSiret: e.detail.value.toString(),
              geographicalCoverage: null,
              service: null,
              formatId: null,
              technicalSource: null,
              tagId: null,
              license: null,
              extraFieldValues: null,
            });
          }}
        />
      </div>

      <div class="fr-col-5 summary__header__buttons">
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
        on:change={(e) => handleFilterChange(e.detail)}
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

  .summary__header__buttons {
    display: flex;
    justify-content: flex-end;
  }

  .fr-btn {
    height: 50px;
  }
</style>
