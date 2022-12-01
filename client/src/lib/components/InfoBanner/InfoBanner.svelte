<div class="info fr-py-1w">
  <div class="fr-container info-container">
    <slot />
  </div>
</div>

<style>
  .info {
    background-color: var(--background-contrast-info);
    color: var(--text-default-info);
  }

  .info-container {
    display: flex;
  }
</style>
