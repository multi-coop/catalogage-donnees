<script lang="ts">
  export let name: string;
  export let src: string;
  export let status: "catalog" | "registered" | "pending";
</script>

<div class="fr-card">
  <div class="fr-card__body">
    <div class="fr-card__content">
      <h3 class="fr-card__title">
        {name}
      </h3>
      <div class="fr-card__start">
        {#if status == "catalog"}
          <p class="fr-badge fr-badge--success">Catalogue activé</p>
        {:else if status == "registered"}
          <p class="fr-badge fr-badge--info">Enregistré</p>
        {:else if status == "pending"}
          <p class="fr-badge fr-badge--new">En cours</p>
        {/if}
      </div>
    </div>
  </div>
  <div class="fr-card__header">
    <div class="fr-card__img">
      <img class="fr-responsive-img fr-p-2w" {src} alt="logo {name}" />
    </div>
  </div>
</div>

<style>
  @media (max-width: 991px) {
    .fr-card__body {
      padding: 0 1rem;
    }
  }
</style>
