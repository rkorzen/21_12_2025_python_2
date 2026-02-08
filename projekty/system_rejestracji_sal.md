# System rejestracji sal na spotkania w firmie

## Opis ogólny
Firma posiada kilka sal konferencyjnych, które pracownicy mogą rezerwować na spotkania. Celem zadania jest stworzenie aplikacji webowej umożliwiającej rezerwację sal, zarządzanie spotkaniami oraz kontrolę dostępności w czasie. System powinien obsługiwać różne role użytkowników i odzwierciedlać typowe potrzeby biurowe.

## Organizacja projektu
Projekt musi być wykonany jako nowy projekt Django, utworzony od zera.
Niedozwolone jest używanie istniejących projektów lub forków jako bazy.
Kod powinien być czytelny, logicznie uporządkowany i zgodny z konwencjami Django.

## Repozytorium
Projekt musi znajdować się w nowym repozytorium Git.
Repozytorium powinno zawierać pełną historię commitów pokazującą postęp pracy.
Gotowe repozytorium należy udostępnić prowadzącemu do sprawdzenia (link do repozytorium).

## Dokumentacja (README)
W repozytorium musi znajdować się plik README.md, który w czytelny sposób opisuje projekt.
README powinno zawierać co najmniej:

- Krótki opis projektu: czym jest aplikacja i jaki problem rozwiązuje.
- Instrukcję uruchomienia projektu lokalnie, obejmującą wymagania (np. Python, Django), sposób instalacji zależności oraz sposób uruchomienia aplikacji.
- Opis funkcjonalności: co użytkownik może zrobić w systemie.
- Instrukcję użytkowania: jak korzystać z aplikacji z perspektywy zwykłego użytkownika i administratora.

Dokumentacja powinna umożliwiać uruchomienie i zrozumienie projektu bez zaglądania w kod.

## Oczekiwania jakościowe
Projekt powinien dać się uruchomić lokalnie bez dodatkowych konfiguracji środowiskowych.
Aplikacja powinna działać zgodnie z opisanymi user stories.
Komunikaty dla użytkownika powinny być czytelne i zrozumiałe.
Rozwiązanie powinno być stabilne i przewidywalne w działaniu.

## User stories – Użytkownik (pracownik)

### Rejestracja i dostęp
- Jako użytkownik chcę móc zalogować się do systemu, aby zarządzać swoimi rezerwacjami.
- Jako użytkownik chcę widzieć tylko te funkcje, do których mam uprawnienia.

### Przegląd sal
- Jako użytkownik chcę zobaczyć listę dostępnych sal, aby wybrać odpowiednią do spotkania.
- Jako użytkownik chcę widzieć podstawowe informacje o sali (np. pojemność, lokalizacja), aby ocenić, czy spełnia moje potrzeby.

### Dostępność i planowanie
- Jako użytkownik chcę sprawdzić dostępność sal w wybranym dniu i przedziale czasu, aby uniknąć konfliktów.
- Jako użytkownik chcę zobaczyć kalendarz rezerwacji sali, aby zaplanować spotkanie z wyprzedzeniem.

### Rezerwacje
- Jako użytkownik chcę zarezerwować salę na konkretną datę i godzinę, aby zorganizować spotkanie.
- Jako użytkownik chcę podać tytuł i opis spotkania, aby inni wiedzieli, czego dotyczy.
- Jako użytkownik chcę widzieć swoje aktualne i przyszłe rezerwacje, aby mieć nad nimi kontrolę.
- Jako użytkownik chcę móc odwołać lub edytować swoją rezerwację, jeśli plany się zmienią.

### Ograniczenia
- Jako użytkownik nie chcę móc zarezerwować sali, która jest już zajęta w danym czasie.
- Jako użytkownik chcę dostać czytelną informację, jeśli próba rezerwacji jest niemożliwa.

## User stories – Administrator

### Zarządzanie salami
- Jako administrator chcę móc dodawać nowe sale, aby system odzwierciedlał rzeczywistą infrastrukturę firmy.
- Jako administrator chcę móc edytować dane sali (np. nazwa, pojemność, dostępność).
- Jako administrator chcę móc dezaktywować salę, jeśli jest czasowo niedostępna (np. remont).

### Zarządzanie rezerwacjami
- Jako administrator chcę mieć wgląd we wszystkie rezerwacje, aby móc reagować na konflikty.
- Jako administrator chcę móc usuwać lub modyfikować dowolną rezerwację, jeśli zachodzi taka potrzeba organizacyjna.
- Jako administrator chcę widzieć historię rezerwacji, aby analizować wykorzystanie sal.

### Kontrola systemu
- Jako administrator chcę mieć możliwość zarządzania użytkownikami, aby kontrolować dostęp do systemu.
- Jako administrator chcę widzieć czytelne komunikaty o błędach i konfliktach, aby łatwo diagnozować problemy.

## Rozszerzenia (opcjonalne)
- Jako użytkownik chcę otrzymać potwierdzenie rezerwacji.
- Jako użytkownik chcę zobaczyć, kto jest organizatorem spotkania (bez wglądu w szczegóły).
- Jako administrator chcę zobaczyć statystyki wykorzystania sal.
- Jako system chcę uniemożliwić rezerwacje w przeszłości.
- Jako system chcę obsługiwać różne strefy czasowe (opcjonalnie).

## Cel zadania
Zadanie ma sprawdzić umiejętność:

- pracy z modelami i relacjami,
- obsługi formularzy,
- walidacji logiki biznesowej,
- rozróżniania ról i uprawnień,
- pracy z czasem i datami,
- tworzenia czytelnego UX bez nadmiaru logiki.
