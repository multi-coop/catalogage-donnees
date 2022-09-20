<script lang="ts">
  import type { TrustedHtml } from "src/lib/util/html";

  export let value: string | TrustedHtml;
</script>

{#if typeof value === "string"}
  {value}
{:else if value.isHtml}
  {@html value.content}
{/if}
