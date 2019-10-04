import { derived } from "svelte/store";
import questions from "./questions";
import index from "./index";

export default derived([questions, index], ([$qs, $i]) => {
    const max = $qs.length;

    if ($i >= max) {
        return $qs[max - 1];
    } else if ($i < 0) {
        return $qs[0];
    }
    return $qs[$i];
});
