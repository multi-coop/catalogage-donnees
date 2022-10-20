<script>
  import { CONTACT_EMAIL } from "src/constants";
</script>

<h1>Page non trouvée</h1>
<p>Erreur 404</p>

<p class="fr-text--lead">
  La page que vous cherchez est introuvable. Veuillez nous excusez pour la gêne
  occasionnée.
</p>

<p>
  Si vous avez tapé l'adresse dans votre navigateur, veuillez vérifier qu'elle
  est correcte. La page n'est peut-être plus disponible. <br />

  Dans ce cas, pour continuer votre visite, vous pouvez visiter notre page
  d'acceuil. <br />

  Sinon, contactez-nous pour que l'on puisse vous rediriger vers la bonne
  information.
</p>

<div class="button-container">
  <div>
    <a class="fr-btn" href="/">Page d'acceuil</a>
  </div>
  <div>
    <a class="fr-btn fr-btn--secondary" href={`mailto:${CONTACT_EMAIL}`}
      >Contactez-nous
    </a>
  </div>
</div>

<style>
  .button-container {
    display: flex;
    gap: 15px;
  }
</style>
