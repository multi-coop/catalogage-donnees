<script lang="ts">
  import type { MaybeHtmlString } from "src/lib/util/maybe";

  /**
   * ASSUMPTION: HTML 'text' comes from a TRUSTED SOURCE, which exempts us
   * from having to sanitize it.
   */
  export let text: MaybeHtmlString;
</script>

{#if typeof text === "string"}
  {text}
{:else}
  {@html text.content}
{/if}
