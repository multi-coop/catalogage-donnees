<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import { Maybe } from "$lib/util/maybe";
  import { capitalize, formatDaysMonthsOrYearsToNow } from "$lib/util/format";
  import DatasetPropertyList from "../DatasetPropertyList/DatasetPropertyList.svelte";

  import logoRepubliqueFrancaise from "$lib/assets/organizations/logoRepubliqueFrancaise.svg";

  export let dataset: Dataset;

  $: properties = [
    {
      label: "Couverture géographique",
      icon: "fr-icon-x-map-2-line",
      value: dataset.geographicalCoverage,
    },
    {
      label: "Formats",
      icon: "fr-icon-file-line",
      value: dataset.formats.map((format) => format.name).join(", "),
    },
    {
      label: "Licence",
      icon: "fr-icon-x-open-data",
      value: Maybe.Some(dataset.license) ? dataset.license : "-",
    },
  ];
</script>

<li>
  <a
    data-test-id="dataset-list-item"
    class="item"
    href={paths.datasetDetail({ id: dataset.id })}
    title="Consulter cette fiche de données"
  >
    <div class="item__logo">
      {#if dataset.catalogRecord.organization.logoUrl}
        <img
          src={dataset.catalogRecord.organization.logoUrl}
          alt={`logo ${dataset.catalogRecord.organization.name}`}
        />
      {:else}
        <img src={logoRepubliqueFrancaise} alt={`logo république française`} />
      {/if}
    </div>

    <div>
      <p class="fr-m-0">
        {#if Maybe.Some(dataset.headlines)}
          <strong data-testid="headlines-title">
            {@html dataset.headlines.title}
          </strong>
        {:else}
          <strong>
            {dataset.title}
          </strong>
        {/if}
      </p>

      <p class="fr-mb-2w fr-text--sm fr-text-mention--grey">
        {dataset.service}
      </p>

      {#if Maybe.Some(dataset.headlines) && Maybe.Some(dataset.headlines.description)}
        <p class="fr-mb-2w fr-text--xs fr-text-mention--grey">
          <em data-testid="headlines-description"
            >... {@html dataset.headlines.description} ...</em
          >
        </p>
      {/if}

      <DatasetPropertyList {properties} />
    </div>

    <div class="item__actions">
      <p class="fr-text--sm">
        {capitalize(
          formatDaysMonthsOrYearsToNow(dataset.catalogRecord.createdAt)
        )}
      </p>

      <span class="fr-icon-arrow-right-line fr-text-label--blue-france" />
    </div>
  </a>
</li>

<style>
  /**
  NOTE:
    (!dsfr) = depends on DSFR implementation, which may change across versions
  */

  .item {
    display: grid;
    column-gap: 1rem;
    grid-template-columns: 1fr 8fr 1fr;
    padding: var(--sp-3w) var(--sp-2w);
  }

  .item[href] {
    background-image: none; /* (!dsfr) */
  }

  .item:hover {
    background-color: var(--background-elevated-grey-hover);
  }
  .item__logo > img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .item__actions {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
  }

  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  p {
    padding: 0;
    margin: 0;
  }
</style>
