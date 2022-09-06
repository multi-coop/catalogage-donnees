<script lang="ts" context="module">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { LoginFormData } from "src/definitions/auth";
  import { login } from "$lib/stores/auth";
  import { loginWithPassword } from "$lib/repositories/auth";
  import LoginForm from "$lib/components/LoginForm/LoginForm.svelte";

  let loading = false;
  let loginFailed = false;

  const onSubmit = async (event: CustomEvent<LoginFormData>) => {
    try {
      loading = true;
      loginFailed = false;

      const response = await loginWithPassword({ fetch, data: event.detail });
      loginFailed = response.status === 401;

      if (loginFailed) {
        return;
      }

      const { account, apiToken } = response.data;

      login(account, apiToken);
      await goto("/");
    } finally {
      loading = false;
    }
  };
</script>

<svelte:head>
  <title>Connexion</title>
</svelte:head>

<section class="fr-container fr-mb-15w">
  <h1 class="fr-grid-row fr-grid-row--center fr-mt-6w">
    Bienvenue sur votre outil de catalogage de données
  </h1>

  <p class="fr-grid-row fr-grid-row--center fr-text--lead fr-mt-6w">
    Connectez-vous à l'espace (démonstration)
  </p>

  <div class="fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-6">
      <LoginForm {loading} {loginFailed} on:submit={onSubmit} />
    </div>
  </div>
</section>
