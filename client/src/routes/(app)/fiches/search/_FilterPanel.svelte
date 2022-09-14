<script lang="ts">
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";
  import type { SelectOption } from "src/definitions/form";
  import type { Tag } from "src/definitions/tag";
  import SearchableSelect from "src/lib/components/SearchableSelect/SearchableSelect.svelte";
  import {
    toFiltersButtonTexts,
    toFiltersOptions,
  } from "src/lib/transformers/datasetFilters";
  import { createEventDispatcher } from "svelte";

  export let info: DatasetFiltersInfo;
  export let value: DatasetFiltersValue;

  const createTagIdToNameMap = (tags: Tag[]) => {
    const map = {};
    tags.forEach(({ id, name }) => (map[id] = name));
    return map;
  };

  $: tagIdToName = createTagIdToNameMap(info.tagId);
  $: filtersOptions = toFiltersOptions(info);
  $: buttonTexts = toFiltersButtonTexts(value, tagIdToName);

  const dispatch = createEventDispatcher<{ change: DatasetFiltersValue }>();

  const handleSelectFilter = <K extends keyof DatasetFiltersValue>(
    key: K,
    e: CustomEvent<SelectOption<DatasetFiltersValue[K]> | null>
  ) => {
    value[key] = e.detail?.value || null;
    dispatch("change", value);
  };
</script>

<section>
  <h6>Informations générales</h6>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Couverture géographique"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.geographicalCoverage || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("geographicalCoverage", e)}
      options={filtersOptions.geographicalCoverage}
    />
  </div>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Service producteur de la donnée"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.service || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("service", e)}
      options={filtersOptions.service}
    />
  </div>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Licence de réutilisation"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.license || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("license", e)}
      options={filtersOptions.license}
    />
  </div>
</section>

<section>
  <h6>Sources et formats</h6>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Format de mise à disposition"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.format || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("format", e)}
      options={filtersOptions.format}
    />
  </div>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Système d'information source"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.technicalSource || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("technicalSource", e)}
      options={filtersOptions.technicalSource}
    />
  </div>
</section>

<section>
  <h6>Mots-clés thématiques</h6>

  <div class="fr-mb-2w">
    <SearchableSelect
      label="Mot-clé"
      buttonPlaceholder="Rechercher..."
      inputPlaceholder="Rechercher..."
      buttonText={buttonTexts.tagId || "Rechercher..."}
      on:clickItem={(e) => handleSelectFilter("tagId", e)}
      options={filtersOptions.tagId}
    />
  </div>
</section>
