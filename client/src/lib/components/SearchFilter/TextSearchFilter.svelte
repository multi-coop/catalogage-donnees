<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import { slugify } from "src/lib/util/format";
  import Basic from "../SearchableComboBox/Basic.svelte";

  import SearchFilterSkeleton from "./SearchFilterSkeleton.svelte";

  export let buttonText: string | null = "";
  export let label: string;
  export let options: SelectOption<any>[];
  export let higlighted = false;

  $: options = [
    {
      label: "Réinistialiser le filtre",
      value: undefined,
    },
    ...options,
  ];

  let showOverLay = false;

  const handleShowOverLay = () => {
    if (!showOverLay) {
      showOverLay = true;
      return;
    }

    if (showOverLay) {
      showOverLay = false;
      return;
    }
  };
</script>

<SearchFilterSkeleton
  {label}
  buttonPlaceholder="Rechercher..."
  buttonText={buttonText || "Rechercher..."}
  isOverlayOpen={showOverLay}
  {higlighted}
  on:mousedown={handleShowOverLay}
>
  <Basic
    on:selectOption
    on:selectOption={() => (showOverLay = false)}
    labelledby={slugify(label)}
    name={slugify(label)}
    on:focusout={handleShowOverLay}
    {options}
  />
</SearchFilterSkeleton>
