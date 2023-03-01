<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  export let label: string;
  export let options: SelectOption[];
  export let name: string;

  let value: "";
</script>

<div class="fr-form-group">
  <legend class="fr-fieldset__legend fr-text--regular" id="radio-legend">
    {label}
  </legend>
  <div class="fr-fieldset__content">
    {#each options as option}
      <div class="fr-radio-group">
        <input
          type="radio"
          id={option.label}
          {name}
          value={option.value}
          bind:group={value}
          on:change
        />
        <label class="fr-label" for={option.label}>{option.label} </label>
      </div>
    {/each}
  </div>
</div>
