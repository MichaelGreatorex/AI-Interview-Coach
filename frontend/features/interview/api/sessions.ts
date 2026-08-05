import { API_BASE_URL } from "../../../client";

export async function deleteSession(
    sessionId: string,
): Promise<void> {
    const response = await fetch(
        `${API_BASE_URL}/sessions/${sessionId}`,
        {
            method: "DELETE",
        },
    );

    if (!response.ok) {
        throw new Error("Failed to delete interview session");
    }
}