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
  import {
    buildActiveFiltersMap,
    getActiveFiltersCount,
    removeNonExistingFiltersValue,
  } from "src/lib/util/datasetFilters";

  export let data: PageData;

  $: ({ paginatedDatasets, q, currentPage, filtersInfo, filtersValue } = data);

  let displayFilters = false;

  export let catalogButtonText = "";

  $: activeFiltersMap = buildActiveFiltersMap(filtersInfo, filtersValue);

  $: activeFiltersCount = getActiveFiltersCount(activeFiltersMap);

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
      ...toFiltersParams(removeNonExistingFiltersValue(filtersValues)),
      makePageParam(1),
    ]);
    goto(href, { noscroll: true });
  };

  const handleClickActiveFilter = (key: string) => {
    handleFilterChange({
      ...filtersValue,
      [key]: null,
    });
  };

  const handleClickExtraFieldActiveFilter = (extrafieldId?: string) => {
    if (!filtersValue.extraFieldValues || !extrafieldId) {
      return;
    }

    const newExtraFieldsValues = filtersValue.extraFieldValues.filter(
      (item) => item.extraFieldId !== extrafieldId
    );

    handleFilterChange({
      ...filtersValue,
      extraFieldValues: newExtraFieldsValues,
    });
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
    <div class="fr-grid-row fr-pb-2w bottom_line">
      <div class="fr-col-7">
        <TextSearchFilter
          higlighted
          label="Catalogue"
          options={filtersInfo.organizationSiret.map(({ name, siret }) => ({
            label: name,
            value: siret,
          }))}
          buttonText={filtersValue.organizationSiret
            ? catalogButtonText
            : "Rechercher..."}
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
          Affiner la recherche {activeFiltersCount > 0
            ? `(${activeFiltersCount})`
            : ""}
        </button>
      </div>
    </div>

    {#if activeFiltersCount > 0}
      <div class="fr-grid-row fr-py-2w bottom_line">
        <div class="fr-col-12">
          <h4 class="fr-h6">Filtres actifs</h4>
          <div role="list">
            {#each Object.entries(activeFiltersMap) as [key, map]}
              {#if map}
                {#if Array.isArray(map)}
                  {#each map as mapItem}
                    <button
                      class="fr-tag fr-icon-close-line fr-tag--icon-left"
                      aria-label={`Retirer ${mapItem.key} : ${mapItem.value}`}
                      on:click|preventDefault={() =>
                        handleClickExtraFieldActiveFilter(mapItem.id)}
                    >
                      {`${mapItem.key} : ${mapItem.value}`}
                    </button>
                  {/each}
                {:else}
                  <button
                    class="fr-tag fr-icon-close-line fr-tag--icon-left"
                    aria-label={`Retirer ${map.key} : ${map.value}`}
                    on:click|preventDefault={() => handleClickActiveFilter(key)}
                  >
                    {`${map.key} : ${map.value}`}
                  </button>
                {/if}
              {/if}
            {/each}
          </div>
        </div>
      </div>
    {/if}

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
  .summary__header__buttons {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }

  .fr-btn {
    height: 50px;
  }

  div[role="list"] {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>
