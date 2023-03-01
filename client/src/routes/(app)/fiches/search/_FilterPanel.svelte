<script lang="ts">
  import type { DataFormat } from "src/definitions/dataformat";
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";
  import type { SelectOption } from "src/definitions/form";
  import type { Organization } from "src/definitions/organization";
  import type { Tag } from "src/definitions/tag";
  import TextSearchFilter from "src/lib/components/SearchFilter/TextSearchFilter.svelte";
  import {
    toFiltersButtonTexts,
    toFiltersOptions,
  } from "src/lib/transformers/datasetFilters";
  import { createEventDispatcher } from "svelte";

  export let info: DatasetFiltersInfo;
  export let value: DatasetFiltersValue;

  const createOrganizationSiretToNameMap = (
    organizations: Organization[]
  ): Record<string, string> => {
    const map = {};
    organizations.forEach(({ siret, name }) => (map[siret] = name));
    return map;
  };

  const createTagIdOrFormatIdToNameMap = (
    items: Tag[] | DataFormat[]
  ): Record<string, string> => {
    const map = {};
    items.forEach(({ id, name }) => (map[id] = name));
    return map;
  };

  $: organizationSiretToName = createOrganizationSiretToNameMap(
    info.organizationSiret
  );
  $: tagIdToName = createTagIdOrFormatIdToNameMap(info.tagId);
  $: formatIdToName = createTagIdOrFormatIdToNameMap(info.formatId);

  $: filtersOptions = toFiltersOptions(info);
  $: buttonTexts = toFiltersButtonTexts(
    value,
    organizationSiretToName,
    tagIdToName,
    formatIdToName
  );

  const dispatch = createEventDispatcher<{ change: DatasetFiltersValue }>();

  const handleSelectFilter = (
    key: string,
    e: CustomEvent<SelectOption<any>>
  ) => {
    value[key] = e.detail?.value || null;
    dispatch("change", value);
  };
</script>

<section>
  <h6>Informations générales</h6>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Couverture géographique"
      options={filtersOptions.geographicalCoverage}
      buttonText={buttonTexts.geographicalCoverage}
      on:selectOption={(e) => handleSelectFilter("geographicalCoverage", e)}
    />
  </div>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Service producteur de la donnée"
      options={filtersOptions.service}
      buttonText={buttonTexts.service}
      on:selectOption={(e) => handleSelectFilter("service", e)}
    />
  </div>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Licence de réutilisation"
      options={filtersOptions.license}
      buttonText={buttonTexts.license}
      on:selectOption={(e) => handleSelectFilter("license", e)}
    />
  </div>

  <h6 class="fr-mt-3w">Catalogues</h6>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Catalogue"
      options={filtersOptions.organizationSiret}
      buttonText={buttonTexts.organizationSiret}
      on:selectOption={(e) => handleSelectFilter("organizationSiret", e)}
    />
  </div>
</section>

<section>
  <h6>Sources et formats</h6>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Format de mise à disposition"
      options={filtersOptions.formatId}
      buttonText={buttonTexts.formatId}
      on:selectOption={(e) => handleSelectFilter("formatId", e)}
    />
  </div>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Système d'information source"
      options={filtersOptions.technicalSource}
      buttonText={buttonTexts.technicalSource}
      on:selectOption={(e) => handleSelectFilter("technicalSource", e)}
    />
  </div>
</section>

<section>
  <h6>Mots-clés thématiques</h6>

  <div class="fr-mb-2w">
    <TextSearchFilter
      label="Mot-clé"
      options={filtersOptions.tagId}
      buttonText={buttonTexts.tagId}
      on:selectOption={(e) => handleSelectFilter("tagId", e)}
    />
  </div>
</section>
