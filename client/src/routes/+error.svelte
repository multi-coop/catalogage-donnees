<script lang="ts" context="module">
  throw new Error("@migration task: Replace error load function (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3293209)");

  // import type { Load } from "@sveltejs/kit";

  // export const load: Load = ({ error, status }) => {
  //   return {
  //     props: {
  //       title: `${status}: ${error ? error.message : "unknown error"}`,
  //     },
  //   };
  // };
</script>

<script lang="ts">
  export let title: string;
</script>

<section class="fr-container fr-mt-9w">
  <h1>{title}</h1>
</section>
