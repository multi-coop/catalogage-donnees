<script lang="ts">
  export let title: string;
</script>

<div class="fr-alert fr-alert--warning">
  <h3 class="fr-alert__title">{title}</h3>
  <p><slot /></p>
</div>
