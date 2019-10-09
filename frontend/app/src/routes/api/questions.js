import axios from "axios";

export async function get(req, res) {
    try {
        const url = `${process.env.API_URL}/api/v1/questions?limit=10`;
        const resp = await axios.get(url);
        res.json(resp.data);
    } catch (error) {
        console.log(error);
        res.statusCode = 500;
        res.end({ error });
    }
}
