<script lang="ts">
  import franceConnect from "$lib/assets/france-connect.svg";
</script>

<div class="mon-compte-pro-container">
  <button aria-label="s'identifier avec Mon Compte Pro" on:click>
    <img class="padlock" alt="" src={franceConnect} />

    <p class="fr-text--md">
      S'identifier avec <br />
      <span class="fr-text--bold">Mon Compte Pro</span>
    </p>
  </button>

  <a href=" http://mon-compte-pro.beta.gouv.fr/" target="_blank">
    Qu'est-ce que Mon Compte Pro ?</a
  >
</div>

<style>
  .mon-compte-pro-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  button {
    background-color: #006adc;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    padding: 5px;
  }

  button:hover {
    background-color: #3e89da;
  }

  p {
    margin: 0;
    padding: 0;
    color: white;
  }
</style>
