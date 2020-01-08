<script context="module">
import questions from "../../../stores/questions";
import fetch from "node-fetch";

async function getResponse(id) {
    try {
        const resp = await fetch(`http://172.105.89.232:5555/api/v1/feedback/${id}`, {
            method: "GET",
            headers: { "Content-Type": "application/json",
            "Authorization": "token a204bbe9-c5fe-4239-b4c8-5e79a6e28a20"},
        });
        return await resp.json();
    } catch (err) {
        console.error(err);
        return [];
    }    
}   
let feedback_text = "xd"
export function getFeedback(id) {
    getResponse(id).then((data) => {
        feedback_text = data["feedback"]
    })
     if (feedback_text == null) {
        return "yo"
    } else {
        return feedback_text
    }
}
</script>




