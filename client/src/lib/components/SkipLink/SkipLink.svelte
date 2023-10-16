<script lang="ts">
  type LinksMap = {
    [linkName: string]: string;
  };

  export let linksMap: LinksMap;
</script>

<div class="fr-skiplinks">
  <nav class="fr-container" aria-label="Accès rapide">
    <ul class="fr-skiplinks__list">
      {#each Object.keys(linksMap) as linkmapKey}
        <li>
          <a class="fr-nav__link" href={`#${linksMap[linkmapKey]}`}
            >{linkmapKey}
          </a>
        </li>
      {/each}
    </ul>
  </nav>
</div>
