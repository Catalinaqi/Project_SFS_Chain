from off_chain.domain.entity.company_entity import CompanyEntity


class CompanyController:

    @staticmethod
    def get_emissions(company_id : int):
        return 0
        #return CompanyEntity.get_company_emission(company_id)

    @staticmethod
    def newCompany(name, address, emissions: int):
        company = CompanyEntity(1,name, address, emissions)
        return 0
        #company.save()