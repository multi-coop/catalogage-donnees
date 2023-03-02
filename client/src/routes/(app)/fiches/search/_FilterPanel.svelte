<script lang="ts">
  import type { ExtraFieldValue } from "src/definitions/catalogs";
  import type { DataFormat } from "src/definitions/dataformat";
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";
  import type { ExtraField } from "src/definitions/extraField";
  import type { SelectOption } from "src/definitions/form";
  import type { Organization } from "src/definitions/organization";
  import type { Tag } from "src/definitions/tag";

  import BooleanSearchFilter from "src/lib/components/SearchFilter/BooleanSearchFilter.svelte";
  import TextSearchFilter from "src/lib/components/SearchFilter/TextSearchFilter.svelte";
  import {
    toFiltersButtonTexts,
    toFiltersOptions,
  } from "src/lib/transformers/datasetFilters";
  import { toSelectOption } from "src/lib/transformers/extraField";
  import { chunk } from "src/lib/util/array";
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

  $: extraFieldChunks = chunk<ExtraField>(info.extraFields, 5);

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

  const handleSelectFilter = <K extends keyof DatasetFiltersValue>(
    key: K,
    e: CustomEvent<SelectOption<any> | null>
  ) => {
    if (key === "organizationSiret" && !e.detail?.value) {
      value.extraFieldValues = null;
    }

    value[key] = e.detail?.value || null;
    dispatch("change", value);
  };

  const removeExistingExtraFieldValue = (
    arr: ExtraFieldValue[],
    id: string
  ) => {
    return arr.filter((obj) => obj.extraFieldId !== id);
  };

  const hasAlreadyTheFilter = (
    extraFieldValues: ExtraFieldValue[],
    id: string
  ) => {
    return extraFieldValues.some((item) => item.extraFieldId === id);
  };

  const handleExtraFieldValueChange = (name: string, event: Event) => {
    const target = event.target as HTMLInputElement;

    let newExtraFieldValues: ExtraFieldValue[] = [];

    if (value.extraFieldValues) {
      if (hasAlreadyTheFilter(value.extraFieldValues, name)) {
        const filteredExtraFields = removeExistingExtraFieldValue(
          value.extraFieldValues,
          name
        );

        newExtraFieldValues = [
          ...filteredExtraFields,
          {
            extraFieldId: name,
            value: target.value,
          },
        ];
      } else {
        newExtraFieldValues = [
          ...value.extraFieldValues,
          {
            extraFieldId: name,
            value: target.value,
          },
        ];
      }
    }

    if (!value.extraFieldValues) {
      newExtraFieldValues = [
        {
          extraFieldId: name,
          value: target.value,
        },
      ];
    }

    value = {
      ...value,
      extraFieldValues: newExtraFieldValues,
    };

    dispatch("change", value);
  };
</script>

<div
  data-test-id="filter-panel"
  class="fr-grid-row fr-grid-row--gutters fitler_section fr-mt-3w"
>
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
</div>
{#if info.extraFields.length > 0 && info.extraFields.some((item) => item.type === "BOOL")}
  <section
    class="fr-py-3w fr-grid-row fr-grid-row--gutters extra_field_filters_section"
  >
    <h6>Champs complémentaires</h6>

    {#each extraFieldChunks as extraFieldChunk}
      <div class="fr-grid-row  extra_field_filter_chunck">
        {#each extraFieldChunk as extraField}
          {#if extraField.type === "BOOL"}
            <BooleanSearchFilter
              name={extraField.name}
              options={toSelectOption(extraField)}
              label={extraField.title}
              on:change={(e) => handleExtraFieldValueChange(extraField.id, e)}
            />
          {/if}
        {/each}
      </div>
    {/each}
  </section>
{/if}

<style>
  .extra_field_filters_section {
    flex-direction: column;
  }

  .fitler_section {
    justify-content: space-between;
  }

  .extra_field_filter_chunck {
    gap: 80px;
  }
</style>
