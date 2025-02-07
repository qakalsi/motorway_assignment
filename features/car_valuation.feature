Feature: Car Valuation Testing
  As a user,
  I want to verify car valuation details,
  So that I can validate registration numbers correctly.

  Scenario Outline: Validate car details for a given registration number
    Given I open the car valuation website
    When I enter "<registration_number>"
    Then I should see the vehicle details "<expected_details>"

    Examples:
      | registration_number | expected_details                          |
      | SG18 HTN           | Volkswagen Golf SE Navigation TSI EVO,2018 |
      | AD58 VNF           | BMW 120D M Sport,2008                      |
      | BW57 BOF           | Toyota Yaris T2,2008                       |
      | KT17 DLX           | Skoda Superb Sportline TDI S-A,2017        |
