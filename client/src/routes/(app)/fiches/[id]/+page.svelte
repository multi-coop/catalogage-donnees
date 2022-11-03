<script lang="ts">
  import type { PageData } from "./$types";
  import paths from "$lib/paths";
  import { DATA_FORMAT_LABELS, UPDATE_FREQUENCY_LABELS } from "src/constants";
  import { formatFullDate, splitParagraphs } from "src/lib/util/format";
  import { account } from "$lib/stores/auth";
  import { Maybe } from "$lib/util/maybe";
  import { canEditDataset } from "$lib/permissions";
  import AsideItem from "./_AsideItem.svelte";
  import ExtraFieldsList from "./_ExtraFieldsList.svelte";
  import { removeEmptyValues } from "src/lib/util/array";
  import { buildMailToString } from "src/lib/util/mail";

  export let data: PageData;

  $: ({ catalog, dataset } = data);

  $: editUrl = Maybe.map(dataset, (dataset) =>
    paths.datasetEdit({ id: dataset.id })
  );

  $: datasetId = Maybe.map(dataset, (dataset) => dataset.id);
</script>

<section class="fr-container">
  {#if Maybe.Some(catalog) && Maybe.Some(dataset) && Maybe.Some(editUrl)}
    <header class="fr-mt-5w">
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-sm-4 fr-col-md-3 fr-col-lg-2">
          <p class="fr-logo" title="république française">
            {@html "Ministère<br />de la culture"}
          </p>
        </div>
        <div class="fr-col-sm-8 fr-col-md-9 fr-col-lg-10">
          <p class="fr-m-0 fr-text-mention--grey">{dataset.service}</p>
          <h1 class="fr-mb-0">
            {dataset.title}
          </h1>
          <div class="header__tags fr-mt-2w">
            {#each dataset.tags as tag}
              <span
                class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon"
              >
                {tag.name}</span
              >
            {/each}
          </div>
        </div>
      </div>

      <ul
        class="fr-grid-row fr-grid-row--right fr-btns-group fr-btns-group--inline fr-btns-group--icon-right fr-my-5w"
      >
        {#if canEditDataset(dataset, $account)}
          <li>
            <a
              href={editUrl}
              class="fr-btn fr-btn--secondary fr-icon-edit-fill"
              title="Modifier ce jeu de données"
            >
              Modifier
            </a>
          </li>
        {/if}
        <li>
          <a
            class="fr-btn fr-btn--secondary fr-icon-mail-line"
            title="Contacter le producteur du jeu de données par email"
            href={buildMailToString(
              removeEmptyValues([
                ...dataset.contactEmails,
                dataset.producerEmail,
              ]),
              `[catalogue.data.gouv.fr] : à propos du jeu de données ${dataset.title}`,
              `Bonjour,%0D%0AJe prends contact avec vous à propos de ce jeu de données : https://catalogue.data.gouv.fr/fiches/${datasetId}.%0D%0A%0D%0A Saisissez votre message ici...`
            )}
          >
            Contacter le producteur
          </a>
        </li>
      </ul>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <aside class="fr-col-md-4">
        <h6 class="fr-mb-2w">Accès aux données</h6>

        <AsideItem
          icon="fr-icon-x-open-data"
          label="Licence de réutilisation"
          value={dataset.license}
        />

        {#if dataset.url}
          <a
            class="fr-btn fr-btn--icon-right fr-icon-external-link-line"
            href={dataset.url}
            target="_blank"
          >
            Voir les données
          </a>
        {/if}

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

        <h6 class="fr-mt-4w fr-mb-2w">Sources et formats</h6>

        <AsideItem
          icon="fr-icon-database-line"
          label="SI source"
          value={dataset.technicalSource}
        />

        <AsideItem
          icon="fr-icon-file-text-line"
          label="Formats disponibles"
          value={dataset.formats.join(", ")}
        >
          <ul class="fr-raw-list">
            {#each dataset.formats as fmt}
              <li>
                {DATA_FORMAT_LABELS[fmt]}
              </li>
            {/each}
          </ul>
        </AsideItem>

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
      </aside>

      <div class="fr-col-md-8">
        <div class="fr-text--sm fr-mb-4w" data-testid="dataset-description">
          {#each splitParagraphs(dataset.description) as text}
            <p class="fr-text--lg">
              {text}
            </p>
          {/each}
        </div>

        {#if catalog.extraFields.length > 0}
          <h6 class="fr-mb-2w">Informations complémentaires</h6>

          <ExtraFieldsList
            extraFields={catalog.extraFields}
            extraFieldValues={dataset.extraFieldValues}
          />
        {/if}
      </div>
    </div>
  {/if}
</section>

<style>
  .fr-logo {
    width: 100%;
    word-break: break-all;
  }

  .header__tags {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
</style>
