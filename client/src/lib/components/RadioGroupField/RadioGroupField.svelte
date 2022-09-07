<script lang="ts">
  import type { SelectOption } from "src/definitions/form";

  export let name: string;
  export let label: string;
  export let hintText: string;
  export let options: SelectOption<string>[];
  export let value: string;

  const clear = () => {
    value = "";
  };
</script>

<div class="fr-form-group">
  <fieldset class="fr-fieldset fr-fieldset--inline">
    <legend class="fr-fieldset__legend fr-text--regular" id="radio-legend">
      {label}
      <span class="fr-hint-text" id="select-hint-{name}-hint">
        {hintText}
      </span>
    </legend>
    <div class="fr-fieldset__content">
      {#each options as option (option.value)}
        {@const id = `${name}-${option.value}`}
        <div class="fr-radio-group">
          <input
            type="radio"
            {id}
            {name}
            value={option.value}
            checked={value === option.value}
            on:change
            on:blur
          />
          <label class="fr-label" for={id}>{option.label} </label>
        </div>
      {/each}
      <button
        type="button"
        class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-mt-2w"
        on:click={clear}
      >
        Effacer
      </button>
    </div>
  </fieldset>
</div>
