<script lang="ts">
  import { Maybe } from "$lib/util/maybe";

  export let icon: string;
  export let label: string;
  export let value: Maybe<string>;
</script>

<div class="aside-item">
  <span class={icon} aria-hidden="true" />

  <div>
    <div class="fr-text--xs fr-my-0 fr-text-mention--grey">
      {label}
    </div>
    <div>
      {#if Maybe.Some(value)}
        <slot>
          {value}
        </slot>
      {:else}
        -
      {/if}
    </div>
  </div>
</div>

<style>
  .aside-item {
    display: flex;
    align-items: center;
    gap: var(--sp-3v);
    margin-bottom: var(--sp-2w);
  }

  .aside-item [class*="fr-icon"] {
    --icon-size: var(--icon-lg);
    color: var(--text-action-high-blue-france);
    margin-top: 0.2rem; /* Adjust vertical alignment */
  }
</style>
