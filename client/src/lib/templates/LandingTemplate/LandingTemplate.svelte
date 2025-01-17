<script lang="ts">
  import { goto } from "$app/navigation";

  import books from "$lib/assets/books-circle.svg";
  import flowChart from "$lib/assets/registration_flow_chart.svg";
  import {
    CONTACT_EMAIL,
    REGISTER_ORGANIZATION_LINK,
    USER_DOCUMENTATION_LINK,
  } from "src/constants";
  import MonCompteProButton from "src/lib/components/MonCompteProButton/MonCompteProButton.svelte";
  import { getApiUrl } from "src/lib/fetch";
  import OrganizationCard from "src/lib/components/OrganizationCard/OrganizationCard.svelte";

  const triggerDataPassLoginFlow = async () => {
    await goto(`${getApiUrl()}/auth/datapass/login/`);
  };
</script>

<section class="banner fr-py-5w fr-md-8w">
  <div class="fr-container">
    <div class="fr-grid-row">
      <div class="fr-col-12 title-container">
        <img class="books-image" alt="" src={books} />

        <div class="fr-mt-3w fr-mt-md-0 fr-ml-md-3w">
          <h1>Bienvenue sur le service de catalogage de données de l’État</h1>
          <p>
            Ce service permet aux administrations centrales et aux opérateurs
            sous leur tutelle de créer, gérer et ouvrir leurs catalogues de
            données dans le cadre notamment de leur stratégie en matière de
            politique de la donnée.
          </p>

          <div class="button-container">
            <MonCompteProButton on:click={triggerDataPassLoginFlow} />
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="fr-container fr-py-8w">
  <h2 class="fr-h3">
    Les organisations enregistrées sur catalogue.data.gouv.fr
  </h2>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Agence de l'environnement et de la maîtrise de l'énergie"
        src={"https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/ademe/logo.svg"}
        status="catalog"
      />
    </div>
    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Agence nationale de l'habitat"
        src={"https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/anah/logo.svg"}
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Centre d'études et d'expertise sur les risques, l'environnement, la mobilité et l'aménagement"
        src={"https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/cerema/logo.svg"}
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Direction de la recherche, des études, de l'évaluation et des statistiques"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/drees/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Direction interministérielle de la transformation publique"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/ditp/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Direction interministérielle du numérique"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/dinum/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Ministère de l’Agriculture et de la Souveraineté alimentaire"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/agriculture/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Ministère de l’Enseignement supérieur et de la Recherche"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/mesr/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Ministère de l’Europe et des Affaires étrangères"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/affaires-etrangeres/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Ministère de la Culture"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/culture/logo.svg"
        status="catalog"
      />
    </div>

    <div class="fr-col-12 fr-col-sm-6 fr-col-md-5 fr-col-lg-3">
      <OrganizationCard
        name="Ministère de la Justice"
        src="https://raw.githubusercontent.com/etalab/catalogage-donnees-config/main/organizations/justice/logo.svg"
        status="catalog"
      />
    </div>
  </div>

  <p class="fr-mt-4w">
    Afin de vous connecter à catalogue.data.gouv.fr, votre organisation doit
    d'abord être enregistrée.
  </p>

  <div>
    <a
      target="_blank"
      rel="noopener"
      class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-edit-fill"
      href={REGISTER_ORGANIZATION_LINK}
      >Guide pour enregistrer son organisation</a
    >
  </div>

  <p class="fr-mt-4w">
    Vous pouvez aussi nous en faire la demande directement :
  </p>

  <div>
    <a
      target="_blank"
      rel="noopener"
      class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-edit-fill"
      href={`mailto:${CONTACT_EMAIL}?subject=Enregistrement sur catalogue.data.gouv.fr&body=Bonjour, je souhaite que mon organisation soit ajoutée sur catalogue.data.gouv.fr...`}
      >catalogue@data.gouv.fr</a
    >
  </div>
</section>

<section class="fr-container fr-mb-6w">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      <h2 class="fr-h3">Comment accéder aux catalogues ?</h2>

      <p>
        L’accès aux catalogues s’effectue via le compte MonComptePro. Il est
        pour l’instant possible uniquement aux agents des organisations
        enregistrées. Pour en savoir plus sur les moyens de s’enregistrer et
        intégrer son catalogue, vous pouvez consulter <a
          class="fr-link"
          target="_blank"
          href={USER_DOCUMENTATION_LINK}>la documentation détaillée</a
        >.
      </p>

      <div class="flow-chart-container fr-pt-5w">
        <img
          class="flow-chart fr-responsive-img"
          alt="Pour pouvoir utiliser cette application vous devez faire partie d'une organisation préalablement enregistrée et avoir créé un compte MonComptePro. Si votre organisation n'est pas encore enregistrée veuillez cliquer sur le lien 'documentation détaillée' pour savoir comment procéder"
          src={flowChart}
        />
      </div>
    </div>
  </div>
</section>

<style>
  .banner {
    background-color: var(--background-alt-blue-france);
  }

  .flow-chart {
    max-width: 30rem;
    height: auto;
  }

  .books-image {
    width: 215px;
    height: 215px;
  }

  .flow-chart-container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .button-container {
    display: flex;
    flex-flow: column;
    gap: var(--sp-3w);
  }

  @media (min-width: 912px) {
    .button-container {
      flex-flow: row;
      gap: var(--sp-1w);
    }
  }
  .title-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  @media (min-width: 768px) {
    .title-container {
      flex-direction: row;
    }
  }
</style>
