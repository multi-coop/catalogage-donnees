import { path } from "./util/paths";

export default {
  home: "/",
  mentionsLegales: "/mentions-legales",
  login: "/login",
  contribute: "/contribuer",
  datasetDetail: path("/fiches/:id"),
  datasetSearch: "/fiches/search",
  datasetEdit: path("/fiches/:id/edit"),
};
