function deleteNote(noteId) {  // Funktion zum Löschen einer Notiz per ID
  fetch("/delete-note", {  // Anfrage an Server senden
    method: "POST",  // HTTP-Methode POST
    body: JSON.stringify({ noteId: noteId }),  // Notiz-ID als JSON senden
  }).then((_res) => {
    window.location.href = "/";  // Seite nach dem Löschen neu laden
  });
}
