<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import { slugify } from "src/lib/util/format";
  export let label: string;
  export let options: SelectOption[];
  export let name: string;

  const createId = ({
    name,
    label,
    value,
  }: {
    name: string;
    label: string;
    value: string;
  }) => {
    return slugify(`${name}-${label}-${value}`);
  };

  let value: "";
</script>

<div class="fr-form-group">
  <legend class="fr-text--regular fr-mb-2w">
    {label}
  </legend>
  <div class="fr-fieldset__content">
    {#each options as option}
      <div class="fr-radio-group">
        <input
          type="radio"
          id={createId({ name, value: option.value, label })}
          {name}
          value={option.value}
          bind:group={value}
          on:change
        />
        <label
          class="fr-label"
          for={createId({ name, value: option.value, label })}
          >{option.label}
        </label>
      </div>
    {/each}
  </div>
</div>
