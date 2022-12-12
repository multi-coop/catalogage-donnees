<script lang="ts">
  import type { ExtraField } from "src/definitions/catalogs";
  import { toSelectOptions } from "src/lib/transformers/form";
  import { renderMarkdown } from "src/lib/util/markdown";
  import InputField from "../InputField/InputField.svelte";
  import RadioGroupField from "../RadioGroupField/RadioGroupField.svelte";
  import Select from "../Select/Select.svelte";

  export let extraField: ExtraField;
  export let value = "";

  // NOTE: hint texts of extra fields are considered TRUSTED as catalogs can
  // only be created via an approved PR on https://github.com/etalab/catalogage-donnees-config.
  $: hintTextHtml = {
    isHtml: true,
    content: renderMarkdown(extraField.hintText),
  };

  const makeBoolOptions = (trueValue: string, falseValue: string) => {
    return toSelectOptions({
      [trueValue]: trueValue,
      [falseValue]: falseValue,
    });
  };

  const makeEnumOptions = (values: string[]) => {
    const map = {};
    values.forEach((value) => (map[value] = value));
    return toSelectOptions(map);
  };
</script>

{#if extraField.type === "TEXT"}
  <InputField
    name={extraField.name}
    label={extraField.title}
    hintText={hintTextHtml}
    bind:value
    on:input
    on:blur
  />
{:else if extraField.type === "BOOL"}
  <RadioGroupField
    name={extraField.name}
    label={extraField.title}
    hintText={hintTextHtml}
    options={makeBoolOptions(
      extraField.data.trueValue,
      extraField.data.falseValue
    )}
    bind:value
    on:change
    on:blur
  />
{:else if extraField.type === "ENUM"}
  <Select
    id={extraField.name}
    name={extraField.name}
    label={extraField.title}
    options={makeEnumOptions(extraField.data.values)}
    hintText={hintTextHtml}
    placeholder={extraField.title}
    bind:value
    on:change
    on:blur
  />
{/if}

<style>
  label > p {
    font-size: inherit;
  }
</style>
