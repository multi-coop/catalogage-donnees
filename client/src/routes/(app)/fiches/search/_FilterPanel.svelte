<script lang="ts">
  import type { ExtraFieldValue } from "src/definitions/catalogs";
  import type { DataFormat } from "src/definitions/dataformat";
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";

  import type { SelectOption } from "src/definitions/form";
  import type { Organization } from "src/definitions/organization";
  import type { Tag } from "src/definitions/tag";

  import BooleanSearchFilter from "src/lib/components/SearchFilter/BooleanSearchFilter.svelte";
  import TextSearchFilter from "src/lib/components/SearchFilter/TextSearchFilter.svelte";
  import {
    toFiltersButtonTexts,
    toFiltersOptions,
  } from "src/lib/transformers/datasetFilters";
  import {
    toSelectOption,
    transformEnumExtraFieldToSelectOptoon,
  } from "src/lib/transformers/extraField";
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

  $: extraFields = info.extraFields.filter(
    (item) => item.type === "ENUM" || item.type == "BOOL"
  );

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

  const handleRadioButtonChange = (extraFieldId: string, event: Event) => {
    const value = (event.target as HTMLInputElement).value;

    handleExtraFieldValueChange(extraFieldId, value);
  };

  const handleExtraFieldValueChange = (
    extraFieldId: string,
    valueFromInput: string | null
  ) => {
    let newExtraFieldValues: ExtraFieldValue[] = [];

    if (!valueFromInput) {
      return;
    }

    if (value.extraFieldValues) {
      if (hasAlreadyTheFilter(value.extraFieldValues, extraFieldId)) {
        const filteredExtraFields = removeExistingExtraFieldValue(
          value.extraFieldValues,
          extraFieldId
        );

        newExtraFieldValues = [
          ...filteredExtraFields,
          {
            extraFieldId: extraFieldId,
            value: valueFromInput,
          },
        ];
      } else {
        newExtraFieldValues = [
          ...value.extraFieldValues,
          {
            extraFieldId: extraFieldId,
            value: valueFromInput,
          },
        ];
      }
    }

    if (!value.extraFieldValues) {
      newExtraFieldValues = [
        {
          extraFieldId: extraFieldId,
          value: valueFromInput,
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

<div data-test-id="filter-panel" class="filter-row fr-mt-2w">
  <section class="filter-col">
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

  <section class="filter-col">
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
  <section class="filter-col">
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
{#if info.extraFields.length > 0}
  <section class="fr-mt-2w">
    <h6>Champs complémentaires</h6>
    <div class="filter-row">
      {#each extraFields as extraField}
        <div class="filter-col">
          {#if extraField.type === "BOOL"}
            <BooleanSearchFilter
              name={extraField.name}
              options={toSelectOption(extraField)}
              label={extraField.title}
              on:change={(e) => handleRadioButtonChange(extraField.id, e)}
            />
          {/if}

          {#if extraField.type === "ENUM"}
            <TextSearchFilter
              label={extraField.title}
              options={transformEnumExtraFieldToSelectOptoon(extraField)}
              on:selectOption={(e) =>
                handleExtraFieldValueChange(extraField.id, `${e.detail.value}`)}
            />
          {/if}
        </div>
      {/each}
    </div>
  </section>
{/if}

<style>
  .filter-row {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .filter-col {
    width: 30%;
  }
</style>
