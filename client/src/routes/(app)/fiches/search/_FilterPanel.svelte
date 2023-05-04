<script lang="ts">
  import type { ExtraFieldValue } from "src/definitions/catalogs";
  import type { DataFormat } from "src/definitions/dataformat";
  import type {
    DatasetFiltersInfo,
    DatasetFiltersValue,
  } from "src/definitions/datasetFilters";
  import type {
    BoolExtraField,
    EnumExtraField,
  } from "src/definitions/extraField";

  import type { SelectOption } from "src/definitions/form";
  import type { Organization } from "src/definitions/organization";
  import type { Tag } from "src/definitions/tag";

  import TextSearchFilter from "src/lib/components/SearchFilter/TextSearchFilter.svelte";
  import {
    toFiltersButtonTexts,
    toFiltersOptions,
  } from "src/lib/transformers/datasetFilters";
  import {
    transformBooleanExtraFieldToSelectOption,
    transformEnumExtraFieldToSelectOption,
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

  const getExtraFieldButtonText = (
    extraField: BoolExtraField | EnumExtraField
  ) => {
    const result = value.extraFieldValues?.find(
      (item) => item.extraFieldId === extraField.id
    );

    return result?.value;
  };

  const handleSelectFilter = <K extends keyof DatasetFiltersValue>(
    key: K,
    e: CustomEvent<SelectOption<any>>
  ) => {
    value[key] = e.detail?.value;
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

  const handleExtraFieldValueChange = (
    extraFieldId: string,
    valueFromInput: string | null
  ) => {
    let newExtraFieldValues: ExtraFieldValue[] = [];

    if (value.extraFieldValues) {
      if (!valueFromInput) {
        const filteredExtraFields = value.extraFieldValues.filter(
          (item) => item.extraFieldId !== extraFieldId
        );

        value = {
          ...value,
          extraFieldValues: filteredExtraFields,
        };

        dispatch("change", value);

        return;
      }
      if (hasAlreadyTheFilter(value.extraFieldValues, extraFieldId)) {
        const filteredExtraFields = removeExistingExtraFieldValue(
          value.extraFieldValues,
          extraFieldId
        );

        newExtraFieldValues = [
          ...filteredExtraFields,
          {
            extraFieldId: extraFieldId,
            value: valueFromInput ?? "",
          },
        ];
      } else {
        newExtraFieldValues = [
          ...value.extraFieldValues,
          {
            extraFieldId: extraFieldId,
            value: valueFromInput ?? "",
          },
        ];
      }
    }

    if (!value.extraFieldValues) {
      newExtraFieldValues = [
        {
          extraFieldId: extraFieldId,
          value: valueFromInput ?? "",
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

<div data-test-id="filter-panel" class="fr-mt-2w">
  <section class="">
    <h3 class="fr-h6">Champs communs</h3>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-4">
        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Couverture géographique"
            options={filtersOptions.geographicalCoverage}
            selected={!!buttonTexts.geographicalCoverage}
            buttonText={buttonTexts.geographicalCoverage}
            on:selectOption={(e) =>
              handleSelectFilter("geographicalCoverage", e)}
          />
        </div>
        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Service producteur de la donnée"
            selected={!!buttonTexts.service}
            options={filtersOptions.service}
            buttonText={buttonTexts.service}
            on:selectOption={(e) => handleSelectFilter("service", e)}
          />
        </div>

        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Licence de réutilisation"
            options={filtersOptions.license}
            selected={!!buttonTexts.license}
            buttonText={buttonTexts.license}
            on:selectOption={(e) => handleSelectFilter("license", e)}
          />
        </div>
      </div>

      <div class="fr-col-4">
        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Format de mise à disposition"
            options={filtersOptions.formatId}
            selected={!!buttonTexts.formatId}
            buttonText={buttonTexts.formatId}
            on:selectOption={(e) => handleSelectFilter("formatId", e)}
          />
        </div>

        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Système d'information source"
            options={filtersOptions.technicalSource}
            buttonText={buttonTexts.technicalSource}
            selected={!!buttonTexts.technicalSource}
            on:selectOption={(e) => handleSelectFilter("technicalSource", e)}
          />
        </div>
      </div>

      <div class="fr-col-4">
        <div class="fr-mb-2w">
          <TextSearchFilter
            label="Mot-clé"
            options={filtersOptions.tagId}
            buttonText={buttonTexts.tagId}
            selected={!!buttonTexts.tagId}
            on:selectOption={(e) => handleSelectFilter("tagId", e)}
          />
        </div>
      </div>
    </div>
  </section>
</div>

{#if info.extraFields.length > 0}
  <section class="fr-my-2w bottom_line-">
    <h6>Champs complémentaires</h6>
    <div class="filter-row">
      {#each extraFields as extraField}
        <div class="filter-col fr-mt-2w">
          {#if extraField.type === "BOOL"}
            <TextSearchFilter
              label={extraField.title}
              options={transformBooleanExtraFieldToSelectOption(extraField)}
              buttonText={getExtraFieldButtonText(extraField)}
              selected={!!getExtraFieldButtonText(extraField)}
              on:selectOption={(e) =>
                handleExtraFieldValueChange(extraField.id, `${e.detail.value}`)}
            />
          {/if}

          {#if extraField.type === "ENUM"}
            <TextSearchFilter
              label={extraField.title}
              buttonText={getExtraFieldButtonText(extraField)}
              selected={!!getExtraFieldButtonText(extraField)}
              options={transformEnumExtraFieldToSelectOption(extraField)}
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
