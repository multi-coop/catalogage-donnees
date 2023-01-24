<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import Tag from "../Tag/Tag.svelte";
  import SearcheableComboBox from "./_SearcheableComboBox.svelte";

  export let options: SelectOption<number>[];
  export let error: string;
  let selectedFormatOptions: SelectOption<number>[] = [];

  const handleSelectFormat = (e: CustomEvent<SelectOption<number>>) => {
    const itemAlreadyExists = selectedFormatOptions.indexOf(e.detail) !== -1;

    if (!itemAlreadyExists) {
      selectedFormatOptions = [...selectedFormatOptions, e.detail];
    }
  };
</script>

<SearcheableComboBox
  label={"Format(s) des données"}
  hintText={"Sélectionnez ici les différents formats de données qu'un réutilisateur potentiel pourrait exploiter."}
  name="dataFormats"
  {options}
  {error}
  on:selectOption={handleSelectFormat}
/>

<div role="list" aria-live="polite">
  {#each selectedFormatOptions as { label, value }}
    <Tag id={value.toString()} name={label} role="list" on:click={() => {}} />
  {/each}
</div>

<style>
  div[role="list"] {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }
</style>
