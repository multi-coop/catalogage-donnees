<script lang="ts">
  export let name: string;
  export let src: string | undefined;
  export let href = "";
  export let status: "catalog" | "registered" | "pending";
</script>

<div class="fr-card fr-card--sm" class:fr-enlarge-link={href}>
  <div class="fr-card__body">
    <div class="fr-card__content">
      <h3 class="fr-card__title">
        {#if href}
          <a {href}>{name}</a>
        {:else}
          {name}
        {/if}
      </h3>
      <div class="fr-card__start">
        <ul class="fr-badge-group">
          <li>
            {#if status == "catalog"}
              <p class="fr-badge fr-badge--success">Catalogue activé</p>
            {:else if status == "registered"}
              <p class="fr-badge fr-badge--info">Enregistré</p>
            {:else if status == "pending"}
              <p class="fr-badge fr-badge--new">Organisation enregistrée</p>
            {/if}
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="fr-card__header">
    <div class="fr-card__img">
      <img class="fr-card__img card-image fr-p-2w" {src} alt="logo {name}" />
    </div>
  </div>
</div>

<style>
  .card-image {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
</style>
