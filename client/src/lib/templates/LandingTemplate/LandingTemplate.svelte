<script lang="ts">
  import { goto } from "$app/navigation";

  import books from "$lib/assets/books-circle.svg";
  import logoMC from "$lib/assets/organizations/logoMC.svg";
  import logoAdeme from "$lib/assets/organizations/logoAdeme.svg";
  import flowChart from "$lib/assets/registration_flow_chart.svg";
  import {
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

<section class="banner fr-py-8w">
  <div class="fr-container">
    <div class="fr-grid-row">
      <div class="fr-col-12 title-container">
        <img class="books-image" alt="" src={books} />

        <div class="fr-pl-3w">
          <h1>Bienvenue sur le service de catalogage de données de l’État</h1>
          <p>
            Ce service permet aux administrations centrales et aux opérateurs
            sous leur tutelle de créer, gérer et ouvrir leurs catalogues de
            données dans le cadre notamment de leur stratégie en matière de
            politique de la donnée.
          </p>

          <p>
            <strong
              >Votre organisation doit être enregistrée pour vous identifier.<strong
              />
            </strong>
          </p>

          <div class="button-container">
            <MonCompteProButton on:click={triggerDataPassLoginFlow} />
            <div>
              <a
                target="_blank"
<<<<<<< HEAD
                rel="noopener"
=======
>>>>>>> 0785ba9 (refacto: rework landing page (add texts, add new schema, ...))
                class="fr-btn fr-btn--secondary fr-btn--icon-right fr-icon-edit-fill"
                href={REGISTER_ORGANIZATION_LINK}
                >Enregistrer mon organisation</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="fr-container fr-py-8w">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      <h3>Comment accéder aux catalogues ?</h3>

      <p>
<<<<<<< HEAD
        L’accès aux catalogues s’effectue via le compte MonComptePro. Il est
=======
        L’accès aux catalogues s’effectue via le compte Mon Compte Pro. Il est
>>>>>>> 0785ba9 (refacto: rework landing page (add texts, add new schema, ...))
        pour l’instant possible uniquement aux agents des organisations
        enregistrées. Pour en savoir plus sur les moyens de s’enregistrer et
        intégrer son catalogue, vous pouvez consulter <a
          class="fr-link"
          target="_blank"
          href={USER_DOCUMENTATION_LINK}>la documentation détaillée</a
        >.
      </p>

      <div class="flow-chart-container fr-pt-5w">
        <img class="flow-chart" alt="" src={flowChart} />
      </div>
    </div>
  </div>
</section>
<section class="fr-container fr-py-8w">
  <h3>Ils utilisent notre service</h3>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-6 fr-col-md-3">
      <OrganizationCard
        name="Ministère de la Culture"
        src={logoMC}
        status="catalog"
      />
    </div>
    <div class="fr-col-6 fr-col-md-3">
      <OrganizationCard name="ADEME" src={logoAdeme} status="pending" />
    </div>
  </div>
</section>

<style>
  .banner {
    background-color: var(--background-alt-blue-france);
  }

  .flow-chart {
    max-width: 350px;
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
    gap: 8px;
  }

  .title-container,
  .button-container {
    display: flex;
  }

  .title-container {
    align-items: center;
    gap: 15px;
  }

  @media (max-width: 991px) {
    .title-container,
    .button-container {
      flex-direction: column;
    }
  }
</style>
