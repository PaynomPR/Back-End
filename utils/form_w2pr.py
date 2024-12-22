def form_w2pr_pdf_generate():
    template = """
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    />
    <title>W2PR-PDF</title>
    <style>
      @page {
        size: A2 landscape;
        font-family: Arial, sans-serif;
      }
      /* Container */
      .container {
        width: 594mm;
        height: 420mm;
        max-width: 100%;
        margin-left: auto;
        margin-right: auto;
      }

      /* Flexbox */
      .flex {
        display: flex;
      }

      .flex-row {
        flex-direction: row;
      }

      .flex-col {
        flex-direction: column;
      }

      /* Margin and Padding */
      .mt-10 {
        margin-top: 2.5rem; /* 10 * 0.25rem */
      }

      .px-2 {
        padding-left: 0.5rem; /* 2 * 0.25rem */
        padding-right: 0.5rem;
      }

      .py-1 {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
      }

      .pb-4 {
        padding-bottom: 1rem; /* 4 * 0.25rem */
      }

      /* Text */
      .text-xs {
        font-size: 1rem;
      }

      .text-sm {
        font-size: 1.2rem;
      }

      .font-semibold {
        font-weight: 600;
      }

      .font-bold {
        font-weight: 700;
      }

      .uppercase {
        text-transform: uppercase;
      }

      /* Borders */


      .border-b-2 {
        border-bottom-width: 1px;
        border-style: solid;
      }

      .border-black {
        border: 1px solid black;

      }

      /* Flex Basis */
      .basis-1-2 {
        flex-basis: 50%;
      }

      .basis-3-5 {
        flex-basis: 60%;
      }

      .basis-2-5 {
        flex-basis: 40%;
      }

      .basis-1-4 {
        flex-basis: 25%;
      }

      /* Text Alignment */
      .text-right {
        text-align: right;
      }

      /* Additional Styles */
      .gap-2 {
        gap: 0.5rem;
      }

      .px-2 {
        padding: 0 4px;
      }

      .pt-1 {
        padding-top: 0.25rem;
      }

      .pt-2 {
        padding-top: 0.5rem; /* 2 * 0.25rem */
      }

      .pt-9 {
        padding-top: 2.25rem; /* 9 * 0.25rem */
      }

      .border-l-2 {
        border-left-width: 2px;
      }

      .border-r-2 {
        border-right-width: 2px;
      }
    </style>
  </head>
  <body>
    <div class="container mx-auto">
      <div class="flex flex-row mt-10">
        <div class="basis-1-2">
          <div class="text-xs font-semibold px-2 pt-1 pb-4">GOBIERNO DE PUERTO RICO- GOVERNMENT OF PUERTO RICO DEPARTAMENTO DE HACIENDA-DEPARTMENT OF THE TREASURY COMPROBANTE DE RETENCIÓN - WITHHOLDING STATEMENT</div>
          <div class="flex flex-row">
            <!-- Parte 1 -->
            <div class="basis-3-5 border-2 border-black flex flex-col">
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">1. Nombre - First Name:</p>
                <p class="uppercase text-sm">{{ name_first_user }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">Apellido(s) - Last Name(s):</p>
                <p class="uppercase text-sm">{{ name_last_user }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  Dirección Postal del Empleado <br />
                  Employee's Mailing Address:
                </p>
                <p class="uppercase text-sm py-6">{{ address_user }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2 flex flex-row">
                <div class="basis-2-5">
                  <p class="text-xs">Fecha de nacimiento:</p>
                  <p class="text-xs">Date of Birth:</p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Dia</p>
                  <p class="text-xs">Day: <b class="px-2 text-sm">{{ date_birth_day }}</b></p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Mes</p>
                  <p class="text-xs">Month: <b class="px-2 text-sm">{{ date_birth_month }}</b></p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Año</p>
                  <p class="text-xs">Year: <b class="px-2 text-sm">{{ date_birth_year }}</b></p>
                </div>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  2. Nombre y Dirección Postal del Patrono <br />
                  Employer's Name and Mailing:
                </p>
                <p class="uppercase text-sm py-6">
                  {{ name_company }} <br />
                  {{ address_company }}
                </p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  Número de Teléfono del Patrono <br />
                  Employer's Telephone Number:
                </p>
                <p class="uppercase text-sm">
                {{ phone_company }}
                </p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  Correo Electrónico del Patrono <br />
                  Employer's E-mail:
                </p>
                <p class="uppercase text-sm">{{ email_company }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2 flex flex-row">
                <div class="basis-2-5">
                  <p class="text-xs">Cese de Operaciones:</p>
                  <p class="text-xs">Cease of Operations:</p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Dia</p>
                  <p class="text-xs">Day:_____</p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Mes</p>
                  <p class="text-xs">Month:____</p>
                </div>
                <div class="basis-1/5">
                  <p class="text-xs">Año</p>
                  <p class="text-xs">Year:_____</p>
                </div>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  Numero Confirmación de Radicación Electronica <br />
                  Electronic Filling Confirmation Number:
                </p>
                <p class="uppercase text-sm"></p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">Numero Control - Control Number:</p>
                <p class="uppercase text-sm">{{n_control}}</p>
              </div>
              <div class="px-2 flex flex-row">
                <div class="basis-3-5 font-bold">
                  <p class="text-xs">Fecha de radicación: 31 de Enero</p>
                  <p class="text-xs">Filling date: January 31</p>
                </div>
                <div class="basis-2-5 flex gap-2 border-l-2 border-black pl-1">
                  <div>
                    <p class="text-xs">Año:</p>
                    <p class="text-xs">Year:</p>
                  </div>
                  <div class="flex w-full font-bold justify-center items-center">
                    <p class="text-xl text-bold uppercase">{{year_active}}</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Parte 2 -->
            <div class="basis-2-5 border-y-2 border-black">
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  3. Núm. Seguro Social <br />
                  Social Security No.:
                </p>
                <p class="uppercase text-sm">{{ social_security_no }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  4. Núm. de Ident. Patronal <br />
                  Employer Ident No. (EIN):
                </p>
                <p class="uppercase text-sm">{{ ein }}</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">
                  5. Costo de cubierta de salud auspiciada por el patrono <br />
                  Cost of employer sponsored health coverage:
                </p>
                <p class="uppercase text-sm text-right">0.00</p>
              </div>
              <div class="border-b-2 py-1 border-black px-2">
                <p class="text-xs">6. Donativo Charitable Contributions</p>
                <p class="uppercase text-sm text-right">{{ total_donation }}</p>
              </div>
              <div class="py-1 px-2 pb-4">
                <p class="text-xs">Indique si la remuneración incluye pagos al empleado por - Indicate if the remuneration includes payments to the employee for:</p>
                <ul
                  style="list-style: upper-alpha"
                  class="pl-4 text-xs"
                >
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Médico cualificado (Ver instrucciones) </label> <br />
                    <label> Qualified physician (See instructions) </label>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Servicios domésticos </label> <br />
                    <label> Domestic service </label>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Trabajo agrícola </label> <br />
                    <label> Agricultural labor </label>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Ministro de una iglesia o miembro de una orden religiosa </label> <br />
                    <label> Minister of a church or a member of a religious order </label>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Profesionales de la salud (Ver instrucciones) </label> <br />
                    <label> Health professionals (See instructions) </label>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Empleo directo (Ver instrucciones) </label> <br />
                    <label> Direct employment (See instructions) </label>
                    <ul>
                      <li>
                        <p class="margin-0">Horas trabajadas</p>
                        <p class="margin-0 flex flex-row">
                          <span class="basis-2-5">Hours worked:</span>
                          <span class="basis-3-5 text-right border-b-2 border-black">{{ total_time_worker }}</span>
                        </p>
                      </li>
                    </ul>
                  </li>
                  <li class="pt-2">
                    <input
                      type="checkbox"
                      disabled
                    />
                    <label> Otros </label> <br />
                    <label> Others:__________________________ </label>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="basis-1-4 flex flex-col border-2 border-black">
          <div class="text-xs font-semibold px-2 border-b-2 border-black pb-4">INFORMACIÓN PARA EL DEPARTAMENTO HACIENDA - DEPARTMENT OF THE TREASURY INFORMATION</div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">7. Sueldos - Wages:</p>
            <p class="uppercase text-sm text-right">{{total_wages}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">8. Comisiones - Commissions:</p>
            <p class="uppercase text-sm text-right">{{total_commissions}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">9. Concesiones - Allowances:</p>
            <p class="uppercase text-sm text-right">{{total_concessions}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">10. Propina - Tips:</p>
            <p class="uppercase text-sm text-right">{{total_tips}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">11. Total = 7 + 8 + 9 + 10:</p>
            <p class="uppercase text-sm text-right">{{total_11}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              12. Gastos Reemb. y Beneficios Marginales <br />
              Reimb. Expenses and Fringe Benefits:
            </p>
            <p class="uppercase text-sm text-right">{{ total_refunds }}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">13. Cont. Retenida - Tax Withheld:</p>
            <p class="uppercase text-sm text-right">{{ total_taxes_pr }}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              14. Fondo de Retiro Gubernamental <br />
              Governmental Retirement Fund:
            </p>
            <p class="uppercase text-sm text-right">0,00</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              15. Aportaciones a Planes Calificados <br />
              Contributions to CODA PLANS:
            </p>
            <p class="uppercase text-sm text-right">0,00</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              Salarios Exentos (Ver instrucciones) <br />
              Exempt Salaries (See instructions)
            </p>
            <div class="flex text-xs flex-row h-9 pt-1">
              <div class="flex items-end justify-end basis-1/12">
                <span class="text-xs">16.</span>
              </div>
              <div class="border-black border-b-2 border-r-2 basis-3-5 flex items-start justify-end">
                <small class="mr-1">Código / Code : {{ code_26 }}</small>
              </div>
              <div class="w-full border-black border-b-2 flex items-end justify-end basic-8/5">{{ total_wages_26 }}</div>
            </div>
            <div class="flex text-xs flex-row h-9 pt-1">
              <div class="flex items-end justify-end basis-1/12">
                <span class="text-xs">17.</span>
              </div>
              <div class="border-black border-b-2 border-r-2 basis-3-5 flex items-start justify-end">
                <small class="mr-1">Código / Code</small>
              </div>
              <div class="w-full border-black border-b-2 flex items-end justify-end basic-8/5">0.0</div>
            </div>
            <div class="flex text-xs flex-row h-9 pt-1">
              <div class="flex items-end justify-end basis-1/12">
                <span class="text-xs">18.</span>
              </div>
              <div class="border-black border-b-2 border-r-2 basis-3-5 flex items-start justify-end">
                <small class="mr-1">Código / Code</small>
              </div>
              <div class="w-full border-black border-b-2 flex items-end justify-end basic-8/5">0.</div>
            </div>
          </div>
          <div class="py-1 px-2">
            <p class="text-xs">19. Aportaciones al Programa Ahorra y Duplica tu Dinero - Contributions to the Save and Double your Money Program:</p>
            <p class="uppercase text-sm text-right">{{ total_aflac }}</p>
          </div>
        </div>
        <div class="basis-1-4 flex-col border-y-2 border-r-2 border-black">
          <div class="text-xs font-semibold px-2 border-b-2 border-black pb-4">INFORMACIÓN PARA EL SEGURO SOCIAL - SOCIAL SECURITY INFORMATION</div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              20. Total Sueldos Seguro social <br />
              Social Security Wages:
            </p>
            <p class="uppercase text-sm text-right pt-9">{{total_20}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              21. Seguro Social Retenido <br />
              Social Security Tax Withheld:
            </p>
            <p class="uppercase text-sm text-right pt-9">{{ total_secures_social }}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              22. Total Sueldos y Pro. Medicare <br />
              Medicare Wages and Tips:
            </p>
            <p class="uppercase text-sm text-right pt-9">{{total_22}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              23. Contrib. Medicare Retenida <br />
              Medicare Tax Withheld:
            </p>
            <p class="uppercase text-sm text-right pt-9">{{ total_medicares }}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">
              24. Propinas Seguro Social <br />
              Social Security Tips:
            </p>
            <p class="uppercase text-sm text-right pt-9">{{total_tips}}</p>
          </div>
          <div class="border-b-2 py-1 border-black px-2">
            <p class="text-xs">25. Seguro Social no Retenido en Propinas - Uncollected Social Security Tax on Tips:</p>
            <p class="uppercase text-sm text-right pt-9">0,00</p>
          </div>
          <div class="py-1 px-2">
            <p class="text-xs">26. Contrib. Medicare no Retenida en Propinas - Uncollected Medicare Tax on Tips:</p>
            <p class="uppercase text-sm text-right">0,00</p>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>

    """
    return template