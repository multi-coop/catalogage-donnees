<script lang="ts">
  import TextOrHtml from "../TextOrHtml/TextOrHtml.svelte";
  import type { TrustedHtml } from "src/lib/util/html";
  import type { SelectOption } from "src/definitions/form";

  export let name: string;
  export let label: string;
  export let hintText: string | TrustedHtml = "";
  export let options: SelectOption<string>[];
  export let value: string;
  export let displayOptionsInline = true;
</script>

<div class="fr-form-group">
  <fieldset
    class="fr-fieldset"
    class:fr-fieldset--inline={displayOptionsInline}
    role="radiogroup"
  >
    <legend class="fr-fieldset__legend fr-text--regular" id="{name}-legend">
      {label}
      {#if hintText}
        <span class="fr-hint-text" id="select-hint-{name}-hint">
          <TextOrHtml value={hintText} />
        </span>
      {/if}
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
          <label class="fr-label" for={id}>{option.label}</label>
        </div>
      {/each}
    </div>
  </fieldset>
</div>
