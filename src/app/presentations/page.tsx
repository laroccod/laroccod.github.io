import { redirect } from "next/navigation";

/** Old-site route: /#/presentations → /papers. */
export default function PresentationsRedirect() {
  redirect("/papers");
}
