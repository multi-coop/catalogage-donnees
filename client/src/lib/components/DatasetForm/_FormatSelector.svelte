<script lang="ts">
  import type { DataFormat } from "src/definitions/dataformat";
  import type { SelectOption } from "src/definitions/form";
  import {
    transformDataFormatToSelectOption,
    transoformSelectOptionToDataFormat,
  } from "src/lib/transformers/form";
  import { createEventDispatcher } from "svelte";
  import Tag from "../Tag/Tag.svelte";
  import SearcheableComboBox from "../SearchableComboBox/SearcheableComboBox.svelte";

  const dispatch = createEventDispatcher<{
    change: Partial<DataFormat>[];
  }>();

  export let formatOptions: DataFormat[];
  export let error: string;

  export let selectedFormatOptions: Partial<DataFormat>[] = [];

  const handleSelectFormat = (e: CustomEvent<SelectOption<number>>) => {
    const selectedOption = transoformSelectOptionToDataFormat(e.detail);

    const itemAlreadyExists =
      selectedFormatOptions.findIndex(
        (item) => item.id == selectedOption.id
      ) !== -1;

    if (!itemAlreadyExists) {
      selectedFormatOptions = [...selectedFormatOptions, selectedOption];

      dispatch("change", selectedFormatOptions);
    }
  };

  const handleRemoveDataFormat = (
    e: CustomEvent<{ id: string; name: string }>
  ) => {
    const filtered = selectedFormatOptions.filter(
      (item) => item.name !== e.detail.name
    );

    selectedFormatOptions = filtered;

    dispatch("change", selectedFormatOptions);
  };

  const handleAddItem = (e: CustomEvent<string>) => {
    selectedFormatOptions = [...selectedFormatOptions, { name: e.detail }];
    dispatch("change", selectedFormatOptions);
  };
</script>

<div class="fr-my-1w">
  <SearcheableComboBox
    label={"Format(s) des données"}
    hintText={"Sélectionnez ici les différents formats de données qu'un réutilisateur potentiel pourrait exploiter."}
    name="dataFormats"
    on:addItem={handleAddItem}
    on:addItem
    options={formatOptions.map(transformDataFormatToSelectOption)}
    {error}
    on:selectOption={handleSelectFormat}
  />

  <div role="list" aria-live="polite">
    {#each selectedFormatOptions as format, index}
      {#if format.name}
        <Tag
          id={`${format.name}-option-${index}`}
          name={format.name}
          role="list"
          on:click={handleRemoveDataFormat}
        />
      {/if}
    {/each}
  </div>
</div>

<style>
  div[role="list"] {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>
