# coding=utf-8
import xmltodict
import pprint
import xlwt


xml_data = """<?xml version="1.0" encoding="gbk"?>
<taxML xsi:type="slSbbtjZzsfpkjmxRequest" version="SW5001-2006" name="slSbbtjZzsfpkjmxRequest" cnName="增值税发票开具明细" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.chinatax.gov.cn/dataspec/">
  <sbbZzsfpkjmx>
    <head>
      <publicHead>
        <nsrsbh>91110302MA0089P12N</nsrsbh>
        <nsrmc>北京车八百科技有限公司</nsrmc>
        <tbrq>2020-05-13</tbrq>
        <sssq>
          <rqQ>20200401</rqQ>
          <rqZ>20200430</rqZ>
        </sssq>
      </publicHead>
    </head>
    <body>
      <zyfpkjmx>
        <mxxx>
          <xh>1</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008435</fphm>
          <kprq>20190924</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>75807.17</je>
          <se>4548.43</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>2</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008436</fphm>
          <kprq>20191010</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>3</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008437</fphm>
          <kprq>20191010</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>4</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008438</fphm>
          <kprq>20191010</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>5</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008439</fphm>
          <kprq>20191010</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>24221.13</je>
          <se>1453.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>6</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008440</fphm>
          <kprq>20191021</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>79107.90</je>
          <se>4746.47</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>7</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008441</fphm>
          <kprq>20191029</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>55834.91</je>
          <se>3350.09</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>8</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008442</fphm>
          <kprq>20191105</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>22245.78</je>
          <se>1334.75</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>9</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008443</fphm>
          <kprq>20191107</kprq>
          <gmfnsrsbh>91320903076399353B</gmfnsrsbh>
          <je>80309.73</je>
          <se>10440.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>10</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008444</fphm>
          <kprq>20191118</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>78412.64</je>
          <se>4704.76</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>11</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008446</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>12</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008447</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>13</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008449</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>14</xh>
          <fpdm>1100183130</fpdm>
          <fphm>25008450</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>15</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632736</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>16</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632737</fphm>
          <kprq>20191127</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>59001.89</je>
          <se>3540.11</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>17</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632741</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>78495.57</je>
          <se>10204.43</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>18</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632742</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>77017.70</je>
          <se>10012.30</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>19</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632743</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>35309.73</je>
          <se>4590.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>20</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632744</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>96826.55</je>
          <se>12587.45</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>21</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632745</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>84734.52</je>
          <se>11015.48</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>22</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632746</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>84668.14</je>
          <se>11006.86</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>23</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632747</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>64800.88</je>
          <se>8424.12</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>24</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632748</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>64800.88</je>
          <se>8424.12</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>25</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632749</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>63013.27</je>
          <se>8191.73</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>26</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632750</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>63013.27</je>
          <se>8191.73</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>27</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632751</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>70628.32</je>
          <se>9181.68</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>28</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632752</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>96088.50</je>
          <se>12491.50</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>29</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632753</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>96088.50</je>
          <se>12491.50</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>30</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632754</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>97663.72</je>
          <se>12696.28</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>31</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632755</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>95575.22</je>
          <se>12424.78</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>32</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632756</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>95575.22</je>
          <se>12424.78</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>33</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632757</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>95575.22</je>
          <se>12424.78</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>34</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632762</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>35</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632763</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>36</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632764</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>37</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632765</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>38</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632766</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>84557.52</je>
          <se>10992.48</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>39</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632767</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>40</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632768</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>41</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632769</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>42</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632770</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>86725.66</je>
          <se>11274.34</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>43</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632771</fphm>
          <kprq>20191215</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>58539.82</je>
          <se>7610.18</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>44</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632772</fphm>
          <kprq>20191217</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>95305.57</je>
          <se>5718.33</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>45</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632773</fphm>
          <kprq>20191217</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>26166.51</je>
          <se>1569.99</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>46</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632774</fphm>
          <kprq>20191217</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>77978.21</je>
          <se>4678.69</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>47</xh>
          <fpdm>1100194130</fpdm>
          <fphm>04632775</fphm>
          <kprq>20191226</kprq>
          <gmfnsrsbh>914201006675575X5</gmfnsrsbh>
          <je>459.62</je>
          <se>27.58</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>48</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852707</fphm>
          <kprq>20200107</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>75471.70</je>
          <se>4528.30</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>49</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852706</fphm>
          <kprq>20200102</kprq>
          <gmfnsrsbh>91110101762151374F</gmfnsrsbh>
          <je>90288.68</je>
          <se>5417.32</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>50</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852708</fphm>
          <kprq>20200107</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>75471.70</je>
          <se>4528.30</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>51</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852709</fphm>
          <kprq>20200107</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>62485.85</je>
          <se>3749.15</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>52</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852710</fphm>
          <kprq>20200110</kprq>
          <gmfnsrsbh>911102285906402340</gmfnsrsbh>
          <je>88495.58</je>
          <se>11504.42</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>53</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852711</fphm>
          <kprq>20200110</kprq>
          <gmfnsrsbh>911102285906402340</gmfnsrsbh>
          <je>88495.58</je>
          <se>11504.42</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>54</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852713</fphm>
          <kprq>20200113</kprq>
          <gmfnsrsbh>9142010066675575X5</gmfnsrsbh>
          <je>459.62</je>
          <se>27.58</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>55</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852714</fphm>
          <kprq>20200113</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>74489.25</je>
          <se>4469.35</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>56</xh>
          <fpdm>1100194130</fpdm>
          <fphm>11852715</fphm>
          <kprq>20200313</kprq>
          <gmfnsrsbh>913702007940387632</gmfnsrsbh>
          <je>2604.53</je>
          <se>156.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>57</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505121</fphm>
          <kprq>20200323</kprq>
          <gmfnsrsbh>91330000767986864U</gmfnsrsbh>
          <je>604.53</je>
          <se>36.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>58</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505122</fphm>
          <kprq>20200326</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>11171.51</je>
          <se>670.29</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>59</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505123</fphm>
          <kprq>20200326</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>52837.78</je>
          <se>3170.27</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>60</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505124</fphm>
          <kprq>20200410</kprq>
          <gmfnsrsbh>91310000710935994Q</gmfnsrsbh>
          <je>37192.45</je>
          <se>2231.55</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>61</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505126</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>62</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505127</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>63</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505128</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>64</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505129</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>65</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505130</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>911201165961263326</gmfnsrsbh>
          <je>94339.62</je>
          <se>5660.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>66</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505131</fphm>
          <kprq>20200506</kprq>
          <gmfnsrsbh>91120118MA06DRHD1P</gmfnsrsbh>
          <je>2827.36</je>
          <se>169.64</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>67</xh>
          <fpdm>1100194130</fpdm>
          <fphm>26505132</fphm>
          <kprq>20200511</kprq>
          <gmfnsrsbh>91110105667530069X</gmfnsrsbh>
          <je>56798.45</je>
          <se>3407.91</se>
          <zfbz>N</zfbz>
        </mxxx>
      </zyfpkjmx>
      <zyfpkjhjxx>
        <zyfpkjhjs>67</zyfpkjhjs>
        <zzszyfphjJe>4817738.52</zzszyfphjJe>
        <zzszyfphjSe>460849.89</zzszyfphjSe>
      </zyfpkjhjxx>
      <ptfpkjmx>
        <mxxx>
          <xh>1</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265570</fphm>
          <kprq>20191112</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>4950.00</je>
          <se>297.00</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>2</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265571</fphm>
          <kprq>20191112</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>589.62</je>
          <se>35.38</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>3</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265573</fphm>
          <kprq>20191122</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>4369.81</je>
          <se>262.19</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>4</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265574</fphm>
          <kprq>20191125</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>700.00</je>
          <se>42.00</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>5</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265575</fphm>
          <kprq>20200102</kprq>
          <gmfnsrsbh>91370900MA3C9U4N8N</gmfnsrsbh>
          <je>223.28</je>
          <se>13.40</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>6</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265576</fphm>
          <kprq>20200103</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>1910.00</je>
          <se>114.60</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>7</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265577</fphm>
          <kprq>20200224</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>65159.43</je>
          <se>3909.57</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>8</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265578</fphm>
          <kprq>20200224</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>59929.25</je>
          <se>3595.75</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>9</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265579</fphm>
          <kprq>20200224</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>55093.40</je>
          <se>3305.60</se>
          <zfbz>N</zfbz>
        </mxxx>
        <mxxx>
          <xh>10</xh>
          <fpdm>0110018001</fpdm>
          <fphm>49265580</fphm>
          <kprq>20200421</kprq>
          <gmfnsrsbh>91120118MA06Q569XG</gmfnsrsbh>
          <je>66913.21</je>
          <se>4014.79</se>
          <zfbz>N</zfbz>
        </mxxx>
      </ptfpkjmx>
      <ptfpkjhjxx>
        <ptfpkjhjs>10</ptfpkjhjs>
        <ptfpkjhjJe>259838.00</ptfpkjhjJe>
        <ptfpkjhjSe>15590.28</ptfpkjhjSe>
      </ptfpkjhjxx>
    </body>
  </sbbZzsfpkjmx>
</taxML>
"""
dict_data = xmltodict.parse(xml_data.strip())
data_list = dict_data.get('taxML').get('sbbZzsfpkjmx')

pprint.pprint(data_list)

#
# # 创建excel
# wb = xlwt.Workbook(encoding='utf-8')
# ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)
#
# # 设置表头
# title = ['发票类型',
#          '发票状态',
#          '发票代码',
#          '发票号码',
#          '上传状态',
#          '客户名称',
#          '主要商品名称',
#          '税额',
#          '合计金额',
#          '价税合计',
#          '原发票代码',
#          '原发票号码',
#          '通知单编号',
#          '开票人',
#          '开票日期',
#          '作废人',
#          '作废日期',
#          '客户识别号',
#          '清单标识',
#          ]
#
# # 生成表头
# len_col = len(title)
# for i in range(0, len_col):
#     ws.write(0, i, title[i])
#
#
# i = 1
# for data in data_list:
#     j = 0
#     for k, v in data.items():
#         ws.write(i, j, v)
#         j += 1
#     i += 1
#
# wb.save(r'd:/che800_fapiao.xls')


