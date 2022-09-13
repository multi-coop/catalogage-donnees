<script context="module" lang="ts">
  throw new Error("@migration task: Check code was safely removed (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292722)");

  // import type { Load } from "@sveltejs/kit";
  // import { get } from "svelte/store";
  // import { getDatasetByID } from "$lib/repositories/datasets";
  // import { apiToken } from "$lib/stores/auth";

  // export const load: Load = async ({ fetch, params }) => {
  //   const dataset = await getDatasetByID({
  //     fetch,
  //     apiToken: get(apiToken),
  //     id: params.id,
  //   });

  //   return {
  //     props: {
  //       dataset,
  //     },
  //   };
  // };
</script>

<script lang="ts">
  throw new Error("@migration task: Add data prop (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292707)");

  import paths from "$lib/paths";
  import { UPDATE_FREQUENCY_LABELS } from "src/constants";
  import type { Dataset } from "src/definitions/datasets";
  import { formatFullDate, splitParagraphs } from "src/lib/util/format";
  import { Maybe } from "$lib/util/maybe";
  import AsideItem from "./_AsideItem.svelte";

  export let dataset: Maybe<Dataset>;

  const editUrl = Maybe.map(dataset, (dataset) =>
    paths.datasetEdit({ id: dataset.id })
  );
</script>

<section class="fr-container">
  {#if Maybe.Some(dataset) && Maybe.Some(editUrl)}
    <header class="fr-mt-5w">
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-sm-4 fr-col-md-3 fr-col-lg-2">
          <p class="fr-logo" title="république française">
            {@html "Ministère<br />de la culture"}
          </p>
        </div>
        <div class="fr-col-sm-8 fr-col-md-9 fr-col-lg-10">
          <p class="fr-m-0 fr-text-mention--grey">Ministère de la culture</p>
          <h1 class="fr-mb-0">
            {dataset.title}
          </h1>
          <div class="header__tags fr-mt-2w">
            {#each dataset.tags as tag}
              <span class="fr-badge fr-badge--info fr-badge--no-icon">
                {tag.name}</span
              >
            {/each}
          </div>
        </div>
      </div>

      <ul
        class="fr-grid-row fr-grid-row--right fr-btns-group fr-btns-group--inline fr-btns-group--icon-right fr-my-5w"
      >
        <li>
          <a
            href={editUrl}
            class="fr-btn fr-btn--secondary fr-icon-edit-fill"
            title="Modifier ce jeu de données"
          >
            Modifier
          </a>
        </li>
        <li>
          <a
            class="fr-btn fr-btn--secondary fr-icon-mail-line"
            title="Contacter le producter du jeu de données par email"
            href="mailto:{dataset.producerEmail}"
          >
            Contacter le producteur
          </a>
        </li>
      </ul>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <aside class="fr-col-md-4">
        <h6 class="fr-mt-4w fr-mb-2w">Informations générales</h6>

        <AsideItem
          icon="fr-icon-bank-line"
          label="Producteur"
          value={dataset.service}
        />

        <AsideItem
          icon="fr-icon-x-map-2-line"
          label="Couverture géographique"
          value={dataset.geographicalCoverage}
        />

        <h6 class="fr-mt-4w fr-mb-2w">Mise à jour</h6>

        <AsideItem
          icon="fr-icon-x-calendar-check-line"
          label="Date de dernière mise à jour"
          value={Maybe.map(dataset.lastUpdatedAt, (v) => formatFullDate(v))}
        />

        <AsideItem
          icon="fr-icon-refresh-line"
          label="Fréquence de mise à jour"
          value={Maybe.map(
            dataset.updateFrequency,
            (v) => UPDATE_FREQUENCY_LABELS[v]
          )}
        />

        <h6 class="fr-mb-2w">Accès aux données</h6>

        <AsideItem
          icon="fr-icon-global-line"
          label="Lien vers les données"
          value={dataset.url}
        >
          <a
            class="fr-btn fr-btn--icon-right fr-icon-external-link-line"
            href={dataset.url}
            target="_blank"
          >
            Voir les données
          </a>
        </AsideItem>

        <AsideItem
          icon="fr-icon-x-open-data"
          label="Licence de réutilisation"
          value={dataset.license}
        />
      </aside>

      <section
        class="fr-col-md-8 fr-text--sm"
        aria-label="Description du jeu de données"
        data-testid="dataset-description"
      >
        {#each splitParagraphs(dataset.description) as text}
          <p class="fr-text--lg">
            {text}
          </p>
        {/each}
      </section>
    </div>
  {/if}
</section>

<style>
  .fr-logo {
    white-space: nowrap;
  }

  .header__tags {
    display: flex;
    gap: 10px;
  }
</style>
