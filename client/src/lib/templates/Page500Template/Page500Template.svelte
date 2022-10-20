<script lang="ts">
  import { CONTACT_EMAIL } from "src/constants";
</script>

<h1>Erreur inattendue</h1>
<p>Erreur 500</p>

<p class="fr-text--lead">
  Désolé le service rencontre un problème innatendu. Nous travaillons pour le
  résoudre le plus rapidement possible.
</p>

<p>
  Essayer de rafraichir la page ou d'essayer plus tard. <br />

  Si vous avez besoin d'une aide dans l'immédiat, veuillez nous contacter
  <br />
</p>

<div class="button-container" />
<div>
  <a class="fr-btn" href={`mailto:${CONTACT_EMAIL}`}>Contactez-nous </a>
</div>

<style>
  .button-container {
    display: flex;
    gap: 15px;
  }
</style>
