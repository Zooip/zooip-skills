# Project docs: files in the repo

How the pre-project skills find a project and write its phase documents.

- **Project**: {{a GitHub milestone or Project, an issue holding the need, or a folder under `.scratch/`}}. The folder for its documents is `docs/projects/<project-slug>/`.
- **Phase documents**: Markdown files in that folder: `01-{{preliminary-study}}.md`, `02-{{exploration}}.md`, `03-{{architecture}}.md`. They are committed and reviewed like code; link them from the project's issue or milestone.
- **Titles**: the first heading of each file: « {{preliminary study title}} », « {{exploration title}} », « {{architecture title}} ».
- **Language**: {{language}}.
- **Diagrams**: Mermaid code blocks, which GitHub and most editors render.
- **Agent notes**: a `<details><summary>Agent notes</summary>` block at the end of the file.
- **Vocabulary source**: {{the glossary from domain.md, or another file}}.
