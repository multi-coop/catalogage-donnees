<script lang="ts">
  import type { ExtraField } from "src/definitions/catalogs";
  import { toSelectOptions } from "src/lib/transformers/form";
  import InputField from "../InputField/InputField.svelte";
  import RadioGroupField from "../RadioGroupField/RadioGroupField.svelte";
  import Select from "../Select/Select.svelte";

  export let extraField: ExtraField;
  export let value: string;

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
    hintText={extraField.hintText}
    bind:value
    on:input
    on:blur
  />
{:else if extraField.type === "BOOL"}
  <RadioGroupField
    name={extraField.name}
    label={extraField.title}
    hintText={extraField.hintText}
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
    hintText={extraField.hintText}
    options={makeEnumOptions(extraField.data.values)}
    bind:value
    on:change
    on:blur
  />
{/if}
