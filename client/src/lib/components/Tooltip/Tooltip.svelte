<script lang="ts">
  export let tooltipContent: string;
</script>

<div
  aria-label={tooltipContent}
  data-microtip-position="top"
  role="tooltip"
  id="tooltip"
>
  <span aria-labelledby="tooltip">
    <slot />
  </span>
</div>
