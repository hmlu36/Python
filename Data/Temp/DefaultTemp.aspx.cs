using System;
using System.Data;
using System.Configuration;
using System.Collections;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using System.Collections.Generic;
using Wuqi.Webdiyer;
using AjaxControlToolkit;
using System.Globalization;
using System.Threading;
using System.Data.SqlClient;
using System.IO;
using ExcelUtilT;
using System.Text;
using System.Collections.Specialized;

public partial class DefaultTemp : JavaScript
{
    #region ----------------全域變數-------------------
    string[] Dist = new string[] { "全部案件", "東區", "南區", "北區", "安平區", "安南區", "中西區", "永康區", "歸仁區", "新化區", "左鎮區", "玉井區", "楠西區", "南化區", "仁德區", "關廟區", "龍崎區", "官田區", "麻豆區", "佳里區", "西港區", "七股區", "將軍區", "學甲區", "北門區", "新營區", "後壁區", "白河區", "東山區", "六甲區", "下營區", "柳營區", "鹽水區", "善化區", "大內區", "山上區", "新市區", "安定區" };
    string[] Area = new string[] { "0,東區", "0,南區", "0,北區", "0,安平區", "0,安南區", "0,中西區", "1,永康區", "1,歸仁區", "1,新化區", "1,左鎮區", "1,玉井區", "1,楠西區", "1,南化區", "1,仁德區", "1,關廟區", "1,龍崎區", "2,官田區", "2,麻豆區", "2,佳里區", "2,西港區", "2,七股區", "2,將軍區", "2,學甲區", "2,北門區", "2,新營區", "2,後壁區", "3,白河區", "3,東山區", "3,六甲區", "3,下營區", "3,柳營區", "3,鹽水區", "3,善化區", "3,大內區", "3,山上區", "3,新市區", "3,安定區" };
    string[,] Area2 = { { "全部案件", "'東區','南區','北區','安平區','安南區','中西區'" }, { "臺南市區", "'東區','南區','北區','安平區','安南區','中西區'" }, { "Mary", "Albert" } };
    ProjectPublic ProjectClass = new ProjectPublic();
    ProjectPublic ProjectClass1 = new ProjectPublic();
    ProjectPublic ProjectClass2 = new ProjectPublic();
    StringBuilder sb = new StringBuilder();
    SqlConnection conn = new SqlConnection(ConfigurationManager.ConnectionStrings["ConnectionString_TncDig"].ConnectionString);
    //public string url = ConfigurationManager.AppSettings["url"];

    string[] areas = { "東區", "南區", "中西區", "北區", "安平區", "安南區", "永康區", "歸仁區", "新化區", "左鎮區", "玉井區", "楠西區", "南化區", "仁德區", "關廟區", "龍崎區", "官田區", "麻豆區", "佳里區", "西港區", "七股區", "將軍區", "學甲區", "北門區", "新營區", "後壁區", "白河區", "東山區", "六甲區", "下營區", "柳營區", "鹽水區", "善化區", "大內區", "山上區", "新市區", "安定區" };
    int[] areaint = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    #endregion

    protected void Page_Load(object sender, EventArgs e)
    {
        //Response.End();
        //Response.Write("ss:" +Session["SSOUser"]);
        //string s ="";
        //if (Session["SSOUser"] != null && Session["SSOUser"].ToString() != "")
        //{
        //  s = Session["SSOUser"].ToString();
        //  //Response.Write(String.Format("s:{0}</br>", Session["SSOUser"]));
        //}
        //Session["SSOUser"] = s;
        //Response.Write(String.Format("sSSOUser:{0}</br>", Session["SSOUser"]));
        /*
        Session.Abandon();
        Session.Clear();
        string[] cookies = Request.Cookies.AllKeys;
        foreach (string cookie in cookies)
        {
            Response.Cookies[cookie].Expires = DateTime.Now.AddDays(-1);
        }
        if (HttpContext.Current != null)
        {
            int cookieCount = HttpContext.Current.Request.Cookies.Count;
            for (var i = 0; i < cookieCount; i++)
            {
                var cookie = HttpContext.Current.Request.Cookies[i];
                if (cookie != null)
                {
                    var cookieName = cookie.Name;
                    var expiredCookie = new HttpCookie(cookieName) { Expires = DateTime.Now.AddDays(-1) };
                    HttpContext.Current.Response.Cookies.Add(expiredCookie); // overwrite it
                }
            }

            // clear cookies server side
            HttpContext.Current.Request.Cookies.Clear();
        }
        */
        if (!IsPostBack)
        {
            hfDate.Value = DateTime.Now.ToShortDateString();

            TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

            #region ----------------案件列表-------------------
            this.GVList_Result_0.Visible = true;
            AspNetPager_Result_0.RecordCount = ApplyListInfo.GetApplyResultCount(Dist[0], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", "");
            BindGrid_Result(Dist[0], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", this.AspNetPager_Result_0, this.GVList_Result_0, "");
            #endregion

            #region-------今日施工---------------
            BindGrid(this.AspNetPager_Result_5, this.GridView0);
            DataTable dt = new DataTable();
            for (int i = 0; i < 6; i++)
                dt.Columns.Add(i.ToString());

            // 2020.02.10 改成從列表結果做統計, 避免分開查詢, 統計與列表筆數不合
            DataSet dta = (DataSet)this.GridView0.DataSource; // getDatatot();
            int tot = 0;
            for (int i = 0; i < 37; i++)
            {
                for (int j = 0; j < dta.Tables[0].Rows.Count; j++)
                {
                    if (areas[i] == dta.Tables[0].Rows[j][1].ToString())
                    {
                        areaint[i] += 1;
                        tot++;
                    }
                }
            }
            dt.Rows.Add(areas[0] + "(" + areaint[0].ToString() + ")", areas[1] + "(" + areaint[1].ToString() + ")", areas[2] + "(" + areaint[2].ToString() + ")", areas[3] + "(" + areaint[3].ToString() + ")", areas[4] + "(" + areaint[4].ToString() + ")", areas[5] + "(" + areaint[5].ToString() + ")");
            dt.Rows.Add(areas[6] + "(" + areaint[6].ToString() + ")", areas[7] + "(" + areaint[7].ToString() + ")", areas[8] + "(" + areaint[8].ToString() + ")", areas[9] + "(" + areaint[9].ToString() + ")", areas[10] + "(" + areaint[10].ToString() + ")", areas[11] + "(" + areaint[11].ToString() + ")");
            dt.Rows.Add(areas[12] + "(" + areaint[12].ToString() + ")", areas[13] + "(" + areaint[13].ToString() + ")", areas[14] + "(" + areaint[14].ToString() + ")", areas[15] + "(" + areaint[15].ToString() + ")", areas[16] + "(" + areaint[16].ToString() + ")", areas[17] + "(" + areaint[17].ToString() + ")");
            dt.Rows.Add(areas[18] + "(" + areaint[18].ToString() + ")", areas[19] + "(" + areaint[19].ToString() + ")", areas[20] + "(" + areaint[20].ToString() + ")", areas[21] + "(" + areaint[21].ToString() + ")", areas[22] + "(" + areaint[22].ToString() + ")", areas[23] + "(" + areaint[23].ToString() + ")");
            dt.Rows.Add(areas[25] + "(" + areaint[25].ToString() + ")", areas[26] + "(" + areaint[26].ToString() + ")", areas[27] + "(" + areaint[27].ToString() + ")", areas[28] + "(" + areaint[28].ToString() + ")", areas[29] + "(" + areaint[29].ToString() + ")", areas[30] + "(" + areaint[30].ToString() + ")");
            dt.Rows.Add(areas[31] + "(" + areaint[31].ToString() + ")", areas[32] + "(" + areaint[32].ToString() + ")", areas[33] + "(" + areaint[33].ToString() + ")", areas[34] + "(" + areaint[34].ToString() + ")", areas[35] + "(" + areaint[35].ToString() + ")", areas[36] + "(" + areaint[36].ToString() + ")");
            dt.Rows.Add(areas[24] + "(" + areaint[24].ToString() + ")", "", "", "", "", "");
            Label16.Text = tot.ToString();
            this.GridView3.DataSource = dt;
            this.GridView3.DataBind();
            #endregion

            #region-------市府工程---------------
            BindGrid2(AspNetPager1, GridView2);
            #endregion

            #region-------缺失違規案件(無使用)---------------
            //BindGridVM(this.AspNetPager_Result_VM, this.GVList_Result_VM);
            #endregion
            #region-------欠繳費用案件(無使用)---------------
            //BindGridAR(this.AspNetPager_Result_AR, this.GVList_Result_AR);
            #endregion
            #region-------抽驗清單(無使用)---------------
            //BindGridRT(this.AspNetPager_Result_RT, this.GVList_Result_RT);
            #endregion
            #region-------加抽驗清單(無使用)---------------
            //BindGridART(this.AspNetPager_Result_ART, this.GVList_Result_ART);
            #endregion

            #region ----------------挖掘整合年度-------------------
            DateTime dt9 = DateTime.Now.AddDays(1);//需要隔日
            int years = dt9.Year;
            int mon = dt9.Month;
            int toyday = dt9.Day;
            //==========年===========
            for (int i = years - 1911 - 3; i < years - 1911 + 3; i++)
            {
                ddl_year.Items.Add(new ListItem(i.ToString(), (i + 1911).ToString()));
            }
            ddl_year.SelectedValue = years.ToString();
            #region-------挖掘整合案件All---------------
            sb = Report3(CombineInforAll(ddl_year.SelectedValue));
            if (sb != null)
            {
                span1.InnerHtml = sb.ToString();
            }
            #endregion
            #endregion

            #region-------路平專案---------------
            BindGridLuPing(this.AspNetPager_Result_LuPing, this.GVList_Result_LuPing);
            #endregion

            #region-------預定施工管制---------------
            BindGridPreCC(this.AspNetPager_Result_PreCC, this.GVList_Result_PreCC);
            #endregion

            #region-------完工禁挖管制---------------
            BindGridCBC(this.AspNetPager_Result_CBC, this.GVList_Result_CBC);
            #endregion

            BindDataList9();
			
        } else if (UnobtrusiveSession.Session["forgeryToken"] != null && !string.IsNullOrEmpty(UnobtrusiveSession.Session["forgeryToken"].ToString())) {
            Response.Write(UnobtrusiveSession.Session["forgeryToken"].ToString());
			Guid session = Guid.Parse(UnobtrusiveSession.Session["forgeryToken"].ToString());
            /*Guid cookie = new Guid(Response.Cookies["AntiforgeryToken"].Value);
            if (session != cookie)
            {
                Session.Abandon();
                //string s = "";
                //if (Session["SSOUser"] != null && Session["SSOUser"].ToString() != "")
                //{
                //  s = Session["SSOUser"].ToString();
                //}
                ////Session.Abandon();
                //Session["SSOUser"] = s;
                Response.Redirect("/TNRoad/html/logout.asp");
            }*/
		}
        
		
		
        
        //hfDate.Value = Session["SSOUser"].ToString();
        GenerateAntiForgeryToken();
        //Session["SSOUser"] = s;
        //Response.Write("sss:" +Session["SSOUser"]);

        csrf_tokenChecker.Check(this, csrf_token);
    }

    public static class csrf_tokenChecker {
        public static void Check(Page page, HiddenField csrf_token) {
            if (!page.IsPostBack) {
                Guid csrf_tokenToken = Guid.NewGuid();
                page.Session["csrf_tokenToken"] = csrf_tokenToken;
                csrf_token.Value = csrf_tokenToken.ToString();
            } else {
                Guid stored = (Guid)page.Session["csrf_tokenToken"];
                Guid sent = new Guid(csrf_token.Value);

                if (sent != stored) {
                    throw new Exception("XSRF Attack Detected!");
                }
            }
        }
    }

    private void GenerateAntiForgeryToken()
	{
        Guid antiforgeryToken = Guid.NewGuid();
        //Cache.Insert("forgeryToken", antiforgeryToken, null,System.Web.Caching.Cache.NoAbsoluteExpiration,TimeSpan.FromMinutes(30));
        UnobtrusiveSession.Session["forgeryToken"] = antiforgeryToken.ToString();
		
        HttpCookie cookie = new HttpCookie("AntiforgeryToken");
        cookie.Value = antiforgeryToken.ToString();
        cookie.Expires = DateTime.Now.AddMinutes(20);
        HttpContext.Current.Response.Cookies.Add(cookie);
	}

	
    #region ----------------(跑馬燈)-------------------
    protected void BindDataList9()
    {
    		/*
        System.DateTime dt2 = System.DateTime.Now;
        TaiwanCalendar tc = new TaiwanCalendar();
        string lastMonth2 = String.Format("{0:D3}", tc.GetYear(dt2)) + String.Format("{0:D2}", tc.GetMonth(dt2)) + String.Format("{0:D2}", tc.GetDayOfMonth(dt2));
        string strSQL2 = "select no, Topic, (convert(varchar,convert(int,substring(convert(varchar,PubDate,101),7,4))-1911))+'/'+substring(convert(varchar,PubDate,101),1,2)+'/'+substring(convert(varchar,PubDate,101),4,2) as PubDate,[Content] from Marquee where (DATEDIFF(day, StopDate, GETDATE()) <= 0)";
        TNrunsql a = new TNrunsql();
        DataTable dt3 = a.selectAll(strSQL2);

        string message = "";
        if (dt3.Rows.Count > 0)
        {
            for (int j = 0; j < dt3.Rows.Count; j++)
            {
                message += "<a href='javascript:opennews2(" + dt3.DefaultView[j]["no"].ToString() + ")'>"+dt3.DefaultView[j]["Topic"].ToString() + "[" + dt3.DefaultView[j]["PubDate"].ToString() + "](" + dt3.DefaultView[j]["Content"].ToString() + ")</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
            }
            if (dt3.Rows.Count<5)
            {

                string strSQL = "SELECT TOP " + (5-dt3.Rows.Count) + " NewsID, Topic, (convert(varchar,convert(int,substring(convert(varchar,PubDate,101),7,4))-1911))+'/'+substring(convert(varchar,PubDate,101),1,2)+'/'+substring(convert(varchar,PubDate,101),4,2) as PubDate FROM Announce WHERE  ((Type = 2) AND (DATEDIFF(day, StopDate, GETDATE()) < 600)) ORDER BY PubDate desc ";
                DataTable dt = a.selectAll(strSQL);
                for (int j = 0; j < dt.Rows.Count; j++)
                {
                    message += "<a href='javascript:opennews(" + dt.DefaultView[j]["NewsID"].ToString() + ")'>"+dt.DefaultView[j]["Topic"].ToString() + "[" + dt.DefaultView[j]["PubDate"].ToString() + "]</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                }
            }
        }
        else
        {
            string strSQL = "SELECT TOP 5 NewsID, Topic, (convert(varchar,convert(int,substring(convert(varchar,PubDate,101),7,4))-1911))+'/'+substring(convert(varchar,PubDate,101),1,2)+'/'+substring(convert(varchar,PubDate,101),4,2) as PubDate FROM Announce WHERE  ((Type = 2) AND (DATEDIFF(day, StopDate, GETDATE()) < 600)) ORDER BY PubDate desc ";
            DataTable dt = a.selectAll(strSQL);
            for (int j = 0; j < dt.Rows.Count; j++)
            {
                message += "<a href='javascript:opennews(" + dt.DefaultView[j]["NewsID"].ToString() + ")'>"+dt.DefaultView[j]["Topic"].ToString() + "[" + dt.DefaultView[j]["PubDate"].ToString() + "]</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
            }
        }
        labPost.Text = message; 
        */

    }
    #endregion

    #region ----------------BindGrid_Result(GW)-------------------
    protected void BindGrid_Result(string DirstName, string Area, AspNetPager AspNetPager_, GridView GVList, string keyWord)
    {
        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();
        List<TNApplyList> applist = ApplyListInfo.GetApplyResults(DirstName, Area, AspNetPager_.StartRecordIndex, AspNetPager_.PageSize, keyWord);
        if (applist.Count > 0)
        {
            GVList.DataSource = applist;
            GVList.DataBind();
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                                "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";
            AspNetPager_.CustomInfoHTML += "&nbsp;案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
        }
        else
        {

        }

        ApplyListInfo.Dispose();
    }
    #endregion

    #region ----------------缺失違規案件(GW)-------------------
    protected void BindGridVM(AspNetPager AspNetPager_, GridView GVList)
    {
        //DataTable dt = new DataTable();
        DataSet dt = new DataSet();
        AspNetPager_.RecordCount = getDataCountVM();
        //dt = getDataVM();
        dt = getDataVM2();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Tables[0].Rows.Count > 0)
        {
            TabContent_Result_VM.Visible = true;
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
            labTextVM.Text = "";
        }
        else
        {
            //GVList.DataSource = dt;
            //GVList.DataBind();
            labTextVM.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
        //meeting_queryList.Dispose();
    }
    protected void AspNetPager_Result_PageChanged_VM(object sender, EventArgs e)
    {
        this.GVList_Result_VM.Visible = true;
        BindGridVM(this.AspNetPager_Result_VM, this.GVList_Result_VM);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountVM()
    {
        string strCmd = "";
        int cou = 0;
        strCmd = "select sum(cou) cou from (SELECT COUNT(*) cou FROM " +
            "dbo.PIPE_CMP INNER JOIN " +
            "dbo.SiteCheck ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.SiteCheck.VCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.SiteCheck.Up_No = dbo.AppUpload.Up_No " +
            "where Case_Type='2' and CheckProc='2' " +
            "UNION " +
            "SELECT COUNT(*) cou " +
            "FROM dbo.PIPE_CMP INNER JOIN " +
            "dbo.MISSINGCASE_P ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.MISSINGCASE_P.MissCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.MISSINGCASE_P.Up_No = dbo.AppUpload.Up_No " +
            "WHERE dbo.AppUpload.Case_Type = '3' AND dbo.MISSINGCASE_P.CheckProc = '1') a";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlDataReader reader = SqlHelper.ExecuteReader(SqlHelper.ConnectionString, CommandType.Text, strCmd))
            {
                if (reader != null)
                {
                    if (reader.Read())
                    {
                        cou = int.Parse(reader["cou"].ToString());
                    }
                }
                else
                {
                    cou = 0;
                }
            }
        }
        catch (Exception)
        {
        }
        return cou;
    }

    private DataTable getDataVM()
    {
        int endIndex = AspNetPager_Result_VM.StartRecordIndex + AspNetPager_Result_VM.PageSize - 1;
        string sqlstr = "";
        sqlstr = "SELECT View_CaseBasic.caseid ,dbo.View_CaseBasic.AppDate,View_CaseBasic.UnitName,dbo.View_CaseBasic.WorkSN, dbo.LicIssue.LicNo, dbo.APPUPLOAD.ViolationCaseNo,APPUPLOAD.MissingCaseNo, dbo.SiteCheck.CheckProc, dbo.PIPE_CMP.PLINE_CMP_ABBR FROM " +
            "dbo.PIPE_CMP INNER JOIN " +
            "dbo.SiteCheck ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.SiteCheck.VCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.SiteCheck.Up_No = dbo.AppUpload.Up_No " +
            //"dbo.USERMANAGER INNER JOIN dbo.PIPE_CMP ON " +
            //"dbo.USERMANAGER.Group_ID = dbo.PIPE_CMP.PLINE_CMP_NO RIGHT OUTER JOIN " +
            //"dbo.AppUpload ON " +
            //"dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            //"dbo.LicIssue INNER JOIN " +
            //"dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            //"dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID LEFT OUTER JOIN " +
            //"dbo.SiteCheck ON " +
            //"dbo.AppUpload.Up_No = dbo.SiteCheck.Up_No " +
            "where 1=1 and Case_Type='2' and CheckProc='2' " +
            "UNION " +
            "SELECT View_CaseBasic.caseid ,dbo.View_CaseBasic.AppDate,View_CaseBasic.UnitName,dbo.View_CaseBasic.WorkSN, dbo.LicIssue.LicNo, dbo.APPUPLOAD.ViolationCaseNo,APPUPLOAD.MissingCaseNo,dbo.MISSINGCASE_P.CheckProc, dbo.PIPE_CMP.PLINE_CMP_ABBR " +
            "FROM dbo.PIPE_CMP INNER JOIN " +
            "dbo.MISSINGCASE_P ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.MISSINGCASE_P.MissCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.MISSINGCASE_P.Up_No = dbo.AppUpload.Up_No " +
            "WHERE dbo.AppUpload.Case_Type = '3' AND " +
            "dbo.MISSINGCASE_P.CheckProc = '1'";
        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY Caseid desc";
        string sqlFormat = string.Format(
       "SELECT * FROM (SELECT row_number() over (ORDER BY AppDate desc) AS RN, " +
       "{1} FROM ({0}) B)C WHERE RN BETWEEN {2} AND {3} {4} ",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_VM.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
    }
    private DataSet getDataVM2()
    {
        int endIndex = AspNetPager_Result_VM.StartRecordIndex + AspNetPager_Result_VM.PageSize - 1;
        string sqlstr = "";
        sqlstr = "SELECT View_CaseBasic.caseid ,dbo.View_CaseBasic.AppDate,View_CaseBasic.UnitName,dbo.View_CaseBasic.WorkSN, dbo.LicIssue.LicNo, dbo.APPUPLOAD.ViolationCaseNo,APPUPLOAD.MissingCaseNo, dbo.SiteCheck.CheckProc, dbo.PIPE_CMP.PLINE_CMP_ABBR FROM " +
            "dbo.PIPE_CMP INNER JOIN " +
            "dbo.SiteCheck ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.SiteCheck.VCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.SiteCheck.Up_No = dbo.AppUpload.Up_No " +
            //"dbo.USERMANAGER INNER JOIN dbo.PIPE_CMP ON " +
            //"dbo.USERMANAGER.Group_ID = dbo.PIPE_CMP.PLINE_CMP_NO RIGHT OUTER JOIN " +
            //"dbo.AppUpload ON " +
            //"dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            //"dbo.LicIssue INNER JOIN " +
            //"dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            //"dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID LEFT OUTER JOIN " +
            //"dbo.SiteCheck ON " +
            //"dbo.AppUpload.Up_No = dbo.SiteCheck.Up_No " +
            "where 1=1 and Case_Type='2' and CheckProc='2' " +
            "UNION " +
            "SELECT View_CaseBasic.caseid ,dbo.View_CaseBasic.AppDate,View_CaseBasic.UnitName,dbo.View_CaseBasic.WorkSN, dbo.LicIssue.LicNo, dbo.APPUPLOAD.ViolationCaseNo,APPUPLOAD.MissingCaseNo,dbo.MISSINGCASE_P.CheckProc, dbo.PIPE_CMP.PLINE_CMP_ABBR " +
            "FROM dbo.PIPE_CMP INNER JOIN " +
            "dbo.MISSINGCASE_P ON " +
            "dbo.PIPE_CMP.PLINE_CMP_NO = dbo.MISSINGCASE_P.MissCaseUnit RIGHT OUTER JOIN " +
            "dbo.USERMANAGER RIGHT OUTER JOIN " +
            "dbo.AppUpload ON " +
            "dbo.USERMANAGER.Emp_Login = dbo.AppUpload.Login_ID LEFT OUTER JOIN " +
            "dbo.LicIssue INNER JOIN " +
            "dbo.View_CaseBasic ON dbo.LicIssue.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.AppUpload.CaseID = dbo.View_CaseBasic.CaseID ON " +
            "dbo.MISSINGCASE_P.Up_No = dbo.AppUpload.Up_No " +
            "WHERE dbo.AppUpload.Case_Type = '3' AND " +
            "dbo.MISSINGCASE_P.CheckProc = '1'";
        //Response.Write(sqlFormat);
        //Response.End();
        DataSet dtt = SqlHelper.ExecuteDataset(SqlHelper.ConnectionString, CommandType.Text, sqlstr); 
        return dtt;
    }

    protected void GVList_Result_VM_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            //缺失違規案號
            Label Lab_VMCaseNo = (Label)e.Row.FindControl("Lab_VMCaseNo");
            Lab_VMCaseNo.Text = DataBinder.Eval(e.Row.DataItem, "CheckProc").ToString().Equals("1") ? DataBinder.Eval(e.Row.DataItem, "MissingCaseNo").ToString() : DataBinder.Eval(e.Row.DataItem, "ViolationCaseNo").ToString();
            //路證號碼
            Label Lab_LicNo = (Label)e.Row.FindControl("Lab_LicNo");
            Lab_LicNo.Text = string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "LicNo").ToString()) ? "無路證號碼" : DataBinder.Eval(e.Row.DataItem, "LicNo").ToString();
            //施工單位
            Label Lab_UnitName = (Label)e.Row.FindControl("Lab_UnitName");
            Lab_UnitName.Text = string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "UnitName").ToString()) ? DataBinder.Eval(e.Row.DataItem, "PLINE_CMP_ABBR").ToString() : DataBinder.Eval(e.Row.DataItem, "UnitName").ToString();
        }
    }
    #endregion

    #region ----------------欠繳費用案件(GW)-------------------
    protected void BindGridAR(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        AspNetPager_.RecordCount = getDataCountAR();
        dt = getDataAR();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Rows.Count > 0)
        {
            TabContent_Result_VM.Visible = true;
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            //GVList.DataSource = dt;
            //GVList.DataBind();
            labTextAR.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
        //meeting_queryList.Dispose();
    }
    protected void AspNetPager_Result_PageChanged_AR(object sender, EventArgs e)
    {
        this.GVList_Result_AR.Visible = true;
        BindGridAR(this.AspNetPager_Result_AR, this.GVList_Result_AR);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountAR()
    {
        int cou = 0;
        string strCmd = "SELECT COUNT(*) cou ";
        strCmd += "FROM dbo.AppBasic INNER JOIN ";
        strCmd += "dbo.PIPE_CMP ON ";
        strCmd += "dbo.AppBasic.AppUnit = dbo.PIPE_CMP.PLINE_CMP_NO RIGHT OUTER JOIN ";
        strCmd += "dbo.LicIssue ON dbo.AppBasic.CaseID = dbo.LicIssue.CaseID ";
        strCmd += "WHERE dbo.LicIssue.IsArrears='Y'";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        //SqlDataReader dr = ProjectClass.getDataReader(strCmd, "1");
        //if (dr != null)
        //{
        //    if (dr.Read())
        //    {
        //        cou = int.Parse(dr["cou"].ToString());
        //        dr.Close();
        //        dr.Dispose();
        //    }
        //}
        //else
        //{
        //    cou = 0;
        //}
        return cou;
    }

    private DataTable getDataAR()
    {
        int endIndex = AspNetPager_Result_AR.StartRecordIndex + AspNetPager_Result_AR.PageSize - 1;
        string sqlstr = "SELECT dbo.LicIssue.ReceiptNo,dbo.LicIssue.CaseID,dbo.LicIssue.LicNo, dbo.PIPE_CMP.PLINE_CMP_ABBR,dbo.PIPE_CMP.PLINE_CMP_NO, dbo.LicIssue.PayDate ";
        sqlstr += "FROM dbo.AppBasic INNER JOIN ";
        sqlstr += "dbo.PIPE_CMP ON ";
        sqlstr += "dbo.AppBasic.AppUnit = dbo.PIPE_CMP.PLINE_CMP_NO RIGHT OUTER JOIN ";
        sqlstr += "dbo.LicIssue ON dbo.AppBasic.CaseID = dbo.LicIssue.CaseID ";
        sqlstr += "WHERE dbo.LicIssue.IsArrears='Y'";
        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY Caseid desc";
        string sqlFormat = string.Format(
       "SELECT * FROM (SELECT row_number() over (ORDER BY PayDate desc) AS RN, " +
       "{1} FROM ({0}) B)C WHERE RN BETWEEN {2} AND {3} {4} ",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_AR.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
        //conn.Open();
        //SqlDataAdapter daa;

        //daa = new SqlDataAdapter(sqlFormat, conn);
        //DataTable dtt = new DataTable();
        //daa.Fill(dtt);

        //daa.Dispose();
        //System.GC.Collect();
        //conn.Close();

        //return dtt;
    }
    protected void GVList_Result_AR_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            //缺失違規案號
            Label Lab_CaseID = (Label)e.Row.FindControl("Lab_CaseID");
            Lab_CaseID.Text = DataBinder.Eval(e.Row.DataItem, "CaseID").ToString();
            //路證號碼
            Label Lab_LicNoAR = (Label)e.Row.FindControl("Lab_LicNoAR");
            Lab_LicNoAR.Text = string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "LicNo").ToString()) ? "無路證號碼" : DataBinder.Eval(e.Row.DataItem, "LicNo").ToString();
            //施工單位
            Label lab_ppcodeName1 = (Label)e.Row.FindControl("lab_ppcodeName1");
            lab_ppcodeName1.Text = DataBinder.Eval(e.Row.DataItem, "PLINE_CMP_ABBR").ToString();
        }
    }
    #endregion

    #region ----------------抽驗清單(GW)-------------------
    protected void BindGridRT(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        AspNetPager_.RecordCount = getDataCountRT();
        dt = getDataRT();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Rows.Count > 0)
        {
            TabContent_Result_VM.Visible = true;
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            //GVList.DataSource = dt;
            //GVList.DataBind();
            labTextRT.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
        //meeting_queryList.Dispose();
    }
    protected void AspNetPager_Result_PageChanged_RT(object sender, EventArgs e)
    {
        this.GVList_Result_RT.Visible = true;
        BindGridRT(this.AspNetPager_Result_RT, this.GVList_Result_RT);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountRT()
    {
        int cou = 0;
        string strCmd = "select COUNT(*) cou from View_CaseTesting where casetype<>'核備' and Posted='Y' and Caseid not in (select Caseid from casecancel where examresult=1) and status<>50";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        //SqlDataReader dr = ProjectClass.getDataReader(strCmd, "1");
        //if (dr != null)
        //{
        //    if (dr.Read())
        //    {
        //        cou = int.Parse(dr["cou"].ToString());
        //        dr.Close();
        //        dr.Dispose();
        //    }
        //}
        //else
        //{
        //    cou = 0;
        //}
        return cou;
    }

    private DataTable getDataRT()
    {
        int endIndex = AspNetPager_Result_RT.StartRecordIndex + AspNetPager_Result_RT.PageSize - 1;
        string sqlstr = "select CaseID,LicNo,unitname,Appdate from View_CaseTesting where casetype<>'核備' and Posted='Y' and Caseid not in (select Caseid from casecancel where examresult=1) and status<>50 ";
        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY Caseid desc";
        string sqlFormat = string.Format(
       "SELECT * FROM (SELECT row_number() over (ORDER BY Appdate desc) AS RN, " +
       "{1} FROM ({0}) B)C WHERE RN BETWEEN {2} AND {3} {4} ",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_RT.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        conn.Open();
        SqlDataAdapter daa;

        daa = new SqlDataAdapter(sqlFormat, conn);
        DataTable dtt = new DataTable();
        daa.Fill(dtt);

        daa.Dispose();
        System.GC.Collect();
        conn.Close();

        return dtt;
    }
    protected void GVList_Result_RT_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            //缺失違規案號
            Label Lab_CaseID_RT = (Label)e.Row.FindControl("Lab_CaseID_RT");
            Lab_CaseID_RT.Text = DataBinder.Eval(e.Row.DataItem, "CaseID").ToString();
            //路證號碼
            Label Lab_LicNoRT = (Label)e.Row.FindControl("Lab_LicNoRT");
            Lab_LicNoRT.Text = string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "LicNo").ToString()) ? "無路證號碼" : DataBinder.Eval(e.Row.DataItem, "LicNo").ToString();
            //施工單位
            Label unitname = (Label)e.Row.FindControl("unitname");
            unitname.Text = DataBinder.Eval(e.Row.DataItem, "unitname").ToString();
        }
    }
    #endregion

    #region ----------------加抽驗清單(GW)-------------------
    protected void BindGridART(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        AspNetPager_.RecordCount = getDataCountART();
        dt = getDataART();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Rows.Count > 0)
        {
            TabContent_Result_VM.Visible = true;
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            //GVList.DataSource = dt;
            //GVList.DataBind();
            labTextART.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
        //meeting_queryList.Dispose();
    }
    protected void AspNetPager_Result_PageChanged_ART(object sender, EventArgs e)
    {
        this.GVList_Result_ART.Visible = true;
        BindGridART(this.AspNetPager_Result_ART, this.GVList_Result_ART);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountART()
    {
        int cou = 0;
        string strCmd = "select COUNT(*) cou from View_CaseTesting where casetype<>'核備' and AddPosted='Y' and Caseid not in (select Caseid from casecancel where examresult=1) and status<>50";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        //SqlDataReader dr = ProjectClass.getDataReader(strCmd, "1");
        //if (dr != null)
        //{
        //    if (dr.Read())
        //    {
        //        cou = int.Parse(dr["cou"].ToString());
        //        dr.Close();
        //        dr.Dispose();
        //    }
        //}
        //else
        //{
        //    cou = 0;
        //}
        return cou;
    }

    private DataTable getDataART()
    {
        int endIndex = AspNetPager_Result_ART.StartRecordIndex + AspNetPager_Result_ART.PageSize - 1;
        string sqlstr = "select * from View_CaseTesting where casetype<>'核備' and AddPosted='Y' and Caseid not in (select Caseid from casecancel where examresult=1) and status<>50 ";
        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY Caseid desc";
        string sqlFormat = string.Format(
       "SELECT * FROM (SELECT row_number() over (ORDER BY Appdate desc) AS RN, " +
       "{1} FROM ({0}) B)C WHERE RN BETWEEN {2} AND {3} {4} ",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_ART.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
        //conn.Open();
        //SqlDataAdapter daa;

        //daa = new SqlDataAdapter(sqlFormat, conn);
        //DataTable dtt = new DataTable();
        //daa.Fill(dtt);

        //daa.Dispose();
        //System.GC.Collect();
        //conn.Close();

        //return dtt;
    }
    protected void GVList_Result_ART_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            //缺失違規案號
            Label Lab_CaseID_ART = (Label)e.Row.FindControl("Lab_CaseID_ART");
            Lab_CaseID_ART.Text = DataBinder.Eval(e.Row.DataItem, "CaseID").ToString();
            //路證號碼
            Label Lab_LicNoART = (Label)e.Row.FindControl("Lab_LicNoART");
            Lab_LicNoART.Text = string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "LicNo").ToString()) ? "無路證號碼" : DataBinder.Eval(e.Row.DataItem, "LicNo").ToString();
            //施工單位
            Label unitnameA = (Label)e.Row.FindControl("unitnameA");
            unitnameA.Text = DataBinder.Eval(e.Row.DataItem, "unitname").ToString();
        }
    }
    #endregion


    #region ----------------挖掘整合-------------------
    public SqlDataReader GetDataReader(String SqlString)
    {
        SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString);
        ConnectionState previousConnectionState = myConnection.State;
        try
        {
            SqlCommand Sqlcmd = new SqlCommand(SqlString, myConnection);
            Sqlcmd.CommandTimeout = 60;
            if (myConnection.State == ConnectionState.Closed)
            {
                myConnection.Open();
            }
            SqlDataReader rd = Sqlcmd.ExecuteReader(CommandBehavior.CloseConnection);
            Sqlcmd.Dispose();

            return rd;
        }
        catch (System.Exception ex)
        {
            return null;
        }
    }

    protected void TabButton_Result_Click_MI(object sender, EventArgs e)
    {
        LinkButton lb = (LinkButton)sender;

        hidMI.Value = lb.Text;
        //Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl("TabContent_Result_MI"));

        // 顯示某個索引標籤內的 Panel 控制項。
        //if (tabPanel != null) tabPanel.Visible = true;

        if (lb.ID == "MI_0")
        {
            sb = Report(CombineInforA(ddl_year.SelectedValue), "(與路平重疊案件)---A表", "LP");
        }
        else if (lb.ID == "MI_1")
        {
            sb = Report(CombineInforB(ddl_year.SelectedValue), "(與年度計畫及新鋪重疊案件)---B表", "YP");
        }
        else if (lb.ID == "MI_2")
        {
            sb = Report(CombineInforC(ddl_year.SelectedValue), "(互相重疊計畫型案件)---C表", "PL");
        }
        else if (lb.ID == "MI_3")
        {
            sb = Report2(CombineInforD(ddl_year.SelectedValue));
        }
        else if (lb.ID == "MI_9")
        {
            sb = Report3(CombineInforAll(ddl_year.SelectedValue));
        }

        if (sb != null)
        {
            span1.InnerHtml = sb.ToString();
        }
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }
    StringCollection CombineInforAll(string selectionFilter)
    {
        StringCollection scNew = new StringCollection();
        try
        {
            //InitializeWebTier ();
            //string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY keep_btime asc) AS RN1,id ApplyNo,plineno ApplyUnit,pj_name PlanName,Area,rpoly PlanScope,keep_btime ScheduledDateS,keep_etime ScheduledDateE,MiningLength DigLength, IntegrationNum from DIGPLAN where (States<>'9' or States is null) and ((convert(int,Substring(keep_btime,1,3))+1911)=" + selectionFilter + " and (convert(int,Substring(keep_etime,1,3))+1911)=" + selectionFilter + ") or ((convert(int,Substring(keep_btime,1,3))+1911)<=" + selectionFilter + " and (convert(int,Substring(keep_etime,1,3))+1911)>" + selectionFilter + ") order by id Desc;";
            string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY keep_btime asc) AS RN1,id ApplyNo,plineno ApplyUnit,pj_name PlanName,Area,rpoly PlanScope,keep_btime ScheduledDateS,keep_etime ScheduledDateE,MiningLength DigLength, IntegrationNum,CONVERT(Varchar,DPD.lat)+',' +CONVERT(varchar,DPD.lng) as latlng from DIGPLAN left join (select Row_Number() over (Partition by Caseid1 order by keep_btime desc) as rnum,lat,lng,caseid1 from DIGPLAN_DIG ) DPD on DIGPLAN.id=DPD.caseid1 and DPD.rnum=1 where (States<>'9' or States is null) and ((convert(int,Substring(keep_btime,1,3))+1911)=" + selectionFilter + " and (convert(int,Substring(keep_etime,1,3))+1911)=" + selectionFilter + ") or ((convert(int,Substring(keep_btime,1,3))+1911)<=" + selectionFilter + " and (convert(int,Substring(keep_etime,1,3))+1911)>" + selectionFilter + ") order by id Desc;";
            //SqlDataReader dr1 = ProjectClass1.getDataReader(strCmd1, "1");
            //SqlDataReader dr1 = GetDataReader(strCmd1);
            SqlDataReader dr1 = SqlHelper.ExecuteReader(SqlHelper.ConnectionString,CommandType.Text,strCmd1);
            while (dr1.Read())
            {
                scNew.Add(dr1["RN1"].ToString() + "※9※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + dr1["ScheduledDateS"].ToString() + "※" + dr1["ScheduledDateE"].ToString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString() + "※" + dr1["latlng"].ToString());
            }
            dr1.Close();
            dr1.Dispose();
            return scNew;
        }
        catch (Exception mge)
        {
            Response.Write(mge.Message);
        }

        return scNew;
    }
    StringCollection CombineInforA(string selectionFilter)
    {
        StringCollection scNew = new StringCollection();
        try
        {
            //InitializeWebTier ();
            string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,A.*,RoadFee.IntegrationNum from IntegrationLP_P A LEFT OUTER JOIN dbo.RoadFee ON A.ApplyNo = dbo.RoadFee.caseid where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            string strCmd2 = "";
            //Response.Write(strCmd1);
            //Response.End();
            //using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            //{
            //    ConnectionState previousConnectionState = myConnection.State;
            //    using (SqlCommand Sqlcmd = new SqlCommand(strCmd1, myConnection))
            //    {
            //        Sqlcmd.CommandTimeout = 60;
            //        if (myConnection.State == ConnectionState.Closed)
            //        {
            //            myConnection.Open();
            //        }
            //        using (SqlDataReader dr1 = Sqlcmd.ExecuteReader())
            //        {
            //            if (dr1 != null)
            //            {
            //                while (dr1.Read())
            //                {
            //                    scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                    strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationLP_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
            //                    using (SqlCommand Sqlcmd2 = new SqlCommand(strCmd2, myConnection))
            //                    {
            //                        Sqlcmd2.CommandTimeout = 60;
            //                        if (myConnection.State == ConnectionState.Closed)
            //                        {
            //                            myConnection.Open();
            //                        }
            //                        using (SqlDataReader dr2 = Sqlcmd2.ExecuteReader())
            //                        {
            //                            if (dr2 != null)
            //                            {
            //                                while (dr2.Read())
            //                                {
            //                                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                                }
            //                            }
            //                        }
            //                    }
            //                }
            //            }
            //        }
            //    }
            //}
            //SqlDataReader dr1 = ProjectClass1.getDataReader(strCmd1, "1");
            SqlDataReader dr1 = SqlHelper.ExecuteReader(SqlHelper.ConnectionString, CommandType.Text, strCmd1);
            //SqlDataReader dr1 = GetDataReader(strCmd1);
            while (dr1.Read())
            {
                scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationLP_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
                //SqlDataReader dr2 = ProjectClass2.getDataReader(strCmd2, "1");
                SqlDataReader dr2 = GetDataReader(strCmd2);
                while (dr2.Read())
                {
                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                }
                dr2.Close();
                dr2.Dispose();
            }
            dr1.Close();
            dr1.Dispose();
            return scNew;
        }
        catch (Exception mge)
        {
            Response.Write(mge.Message);
        }

        return scNew;
    }
    StringCollection CombineInforB(string selectionFilter)
    {
        StringCollection scNew = new StringCollection();
        try
        {
            //InitializeWebTier ();
            //string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,* from IntegrationYP_P A where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,A.*,RoadFee.IntegrationNum from IntegrationYP_P A LEFT OUTER JOIN dbo.RoadFee ON A.ApplyNo = dbo.RoadFee.caseid where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            string strCmd2 = "";
            //using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            //{
            //    ConnectionState previousConnectionState = myConnection.State;
            //    using (SqlCommand Sqlcmd = new SqlCommand(strCmd1, myConnection))
            //    {
            //        Sqlcmd.CommandTimeout = 60;
            //        if (myConnection.State == ConnectionState.Closed)
            //        {
            //            myConnection.Open();
            //        }
            //        using (SqlDataReader dr1 = Sqlcmd.ExecuteReader())
            //        {
            //            if (dr1 != null)
            //            {
            //                while (dr1.Read())
            //                {
            //                    scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                    // strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,* from IntegrationYP_S B where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
            //                    strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationYP_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
            //                    using (SqlCommand Sqlcmd2 = new SqlCommand(strCmd2, myConnection))
            //                    {
            //                        Sqlcmd2.CommandTimeout = 60;
            //                        if (myConnection.State == ConnectionState.Closed)
            //                        {
            //                            myConnection.Open();
            //                        }
            //                        using (SqlDataReader dr2 = Sqlcmd2.ExecuteReader())
            //                        {
            //                            if (dr2 != null)
            //                            {
            //                                while (dr2.Read())
            //                                {
            //                                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                                }
            //                            }
            //                        }
            //                    }
            //                }
            //            }
            //        }
            //    }
            //}
            //SqlDataReader dr1 = ProjectClass1.getDataReader(strCmd1, "1");
            SqlDataReader dr1 = SqlHelper.ExecuteReader(SqlHelper.ConnectionString, CommandType.Text, strCmd1);
            //SqlDataReader dr1 = GetDataReader(strCmd1);
            while (dr1.Read())
            {
                scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,* from IntegrationYP_S B where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
                strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationYP_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
                SqlDataReader dr2 = GetDataReader(strCmd2);
                //SqlDataReader dr2 = ProjectClass2.getDataReader(strCmd2, "1");
                while (dr2.Read())
                {
                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                }
                dr2.Close();
                dr2.Dispose();
            }
            dr1.Close();
            dr1.Dispose();
            return scNew;
        }
        catch (Exception mge)
        {
            Response.Write(mge.Message);
        }

        return scNew;
    }
    StringCollection CombineInforC(string selectionFilter)
    {
        StringCollection scNew = new StringCollection();
        try
        {
            //InitializeWebTier ();
            //string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,* from IntegrationPL_P A where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,A.*,DIGPLAN.IntegrationNum from IntegrationPL_P A LEFT OUTER JOIN dbo.DIGPLAN ON A.ApplyNo = dbo.DIGPLAN.id where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            string strCmd2 = "";
            //using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            //{
            //    ConnectionState previousConnectionState = myConnection.State;
            //    using (SqlCommand Sqlcmd = new SqlCommand(strCmd1, myConnection))
            //    {
            //        Sqlcmd.CommandTimeout = 60;
            //        if (myConnection.State == ConnectionState.Closed)
            //        {
            //            myConnection.Open();
            //        }
            //        using (SqlDataReader dr1 = Sqlcmd.ExecuteReader())
            //        {
            //            if (dr1 != null)
            //            {
            //                while (dr1.Read())
            //                {
            //                    scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                    //strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,* from IntegrationPL_S B where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
            //                    strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationPL_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
            //                    using (SqlCommand Sqlcmd2 = new SqlCommand(strCmd2, myConnection))
            //                    {
            //                        Sqlcmd2.CommandTimeout = 60;
            //                        if (myConnection.State == ConnectionState.Closed)
            //                        {
            //                            myConnection.Open();
            //                        }
            //                        using (SqlDataReader dr2 = Sqlcmd2.ExecuteReader())
            //                        {
            //                            if (dr2 != null)
            //                            {
            //                                while (dr2.Read())
            //                                {
            //                                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
            //                                }
            //                            }
            //                        }
            //                    }
            //                }
            //            }
            //        }
            //    }
            //}
            //SqlDataReader dr1 = ProjectClass1.getDataReader(strCmd1, "1");
            SqlDataReader dr1 = SqlHelper.ExecuteReader(SqlHelper.ConnectionString, CommandType.Text, strCmd1);
            //SqlDataReader dr1 = GetDataReader(strCmd1);
            while (dr1.Read())
            {
                scNew.Add(dr1["RN1"].ToString() + "※1※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr1["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                //strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,* from IntegrationPL_S B where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
                strCmd2 = "select ROW_NUMBER() OVER(ORDER BY B.[ScheduledDateS] asc) AS RN2,B.*,DIGPLAN.IntegrationNum from dbo.IntegrationPL_S AS B LEFT OUTER JOIN dbo.DIGPLAN ON B.ApplyNo = dbo.DIGPLAN.id where IntegrationID='" + dr1["ApplyNo"].ToString() + "';";
                //SqlDataReader dr2 = ProjectClass2.getDataReader(strCmd2, "1");
                SqlDataReader dr2 = GetDataReader(strCmd2);
                while (dr2.Read())
                {
                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr2["ApplyNo"].ToString() + "※" + dr2["ApplyUnit"].ToString() + "※" + dr2["PlanName"].ToString() + "※" + dr2["Area"].ToString() + "※" + dr2["PlanScope"].ToString() + "※" + DateTime.Parse(dr2["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr2["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr2["DigLength"].ToString() + "※&nbsp;※&nbsp;" + "※" + dr2["IntegrationNum"].ToString() + "※" + dr1["ApplyNo"].ToString());
                }
                dr2.Close();
                dr2.Dispose();
            }
            dr1.Close();
            dr1.Dispose();
            return scNew;
        }
        catch (Exception mge)
        {
            Response.Write(mge.Message);
        }

        return scNew;
    }
    StringCollection CombineInforD(string selectionFilter)
    {
        StringCollection scNew = new StringCollection();
        try
        {
            string strCmd1 = "select ROW_NUMBER() OVER(ORDER BY A.[ScheduledDateS] asc) AS RN1,* from IntegrationPL A where (year(ScheduledDateS)=" + selectionFilter + " and year(ScheduledDateE)=" + selectionFilter + ") or (year(ScheduledDateS)<=" + selectionFilter + " and year(ScheduledDateE)>" + selectionFilter + ");";
            //using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            //{
            //    ConnectionState previousConnectionState = myConnection.State;
            //    using (SqlCommand Sqlcmd = new SqlCommand(strCmd1, myConnection))
            //    {
            //        Sqlcmd.CommandTimeout = 60;
            //        if (myConnection.State == ConnectionState.Closed)
            //        {
            //            myConnection.Open();
            //        }
            //        using (SqlDataReader dr1 = Sqlcmd.ExecuteReader())
            //        {
            //            if (dr1 != null)
            //            {
            //                while (dr1.Read())
            //                {
            //                    scNew.Add(dr1["RN1"].ToString() + "※0※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;※&nbsp");
            //                }
            //            }
            //        }
            //    }
            //}
            //SqlDataReader dr1 = ProjectClass1.getDataReader(strCmd1, "1");
            SqlDataReader dr1 = SqlHelper.ExecuteReader(SqlHelper.ConnectionString, CommandType.Text, strCmd1);
            //SqlDataReader dr1 = GetDataReader(strCmd1);
            while (dr1.Read())
            {
                scNew.Add(dr1["RN1"].ToString() + "※0※" + dr1["ApplyNo"].ToString() + "※" + dr1["ApplyUnit"].ToString() + "※" + dr1["PlanName"].ToString() + "※" + dr1["Area"].ToString() + "※" + dr1["PlanScope"].ToString() + "※" + DateTime.Parse(dr1["ScheduledDateS"].ToString()).ToShortDateString() + "※" + DateTime.Parse(dr1["ScheduledDateE"].ToString()).ToShortDateString() + "※" + dr1["DigLength"].ToString() + "※&nbsp;※&nbsp;※&nbsp");
            }
            dr1.Close();
            dr1.Dispose();
            return scNew;
        }
        catch (Exception mge)
        {
            Response.Write(mge.Message);
        }

        return scNew;
    }
    public StringBuilder Report(StringCollection sc, String titleStr, string species)
    {
        StringBuilder sb = new StringBuilder();
        #region 表尾合計

        int CountRow1 = 0;
        int CountRow2 = 0;
        int CountRow3 = 0;
        int CountRow4 = 0;
        int CountRow5 = 0;
        int CountRow6 = 0;
        int CountRow7 = 0;
        int CountRow8 = 0;
        int CountRow9 = 0;

        #endregion


        #region 表頭
        sb.Append("<table class=\"GridViewStyle\"  rules=\"all\" id='TABLE1' border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width='98%'>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<td  colspan='13' align='center'>");
        sb.Append((int.Parse(ddl_year.SelectedValue) - 1911).ToString() + " 年計畫性挖掘初步整合會議資料表" + titleStr + "</td>");
        sb.Append("</tr>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<th scope=\"col\" >項目</th>");
        sb.Append("<th scope=\"col\" >申請編號</th>");
        sb.Append("<th scope=\"col\" style=\"width:30%;\">申請/協辦單位</th>");
        sb.Append("<th scope=\"col\" >主</th>");
        sb.Append("<th scope=\"col\" >從</th>");
        sb.Append("<th scope=\"col\" style=\"width:30%;\">計畫名稱</th>");
        sb.Append("<th scope=\"col\" >行政區</th>");
        sb.Append("<th scope=\"col\" style=\"width:30%;\">計畫範圍</th>");
        sb.Append("<th scope=\"col\" >預定工期</th>");
        sb.Append("<th scope=\"col\" >挖掘長度</th>");
        sb.Append("<th scope=\"col\" >最遲送件時程</th>");
        sb.Append("<th scope=\"col\" >協調應辦事項</th>");
        sb.Append("<th scope=\"col\" >整合編號</th>");
        //sb.Append("<td style=\"border-color : Black;border-style : solid;border-top-width :0.3mm;border-right-width : 0.3mm;border-left-width : 0.3mm;border-bottom-width : 0.3mm;\" class=\"Noprint\" align='center'>套疊圖</td>");
        sb.Append("</tr>");

        #endregion

        StringCollection scKey = new StringCollection();
        #region 內容
        //-------------------------------------------------------
        int o = 1;
        int no = 1;
        string style = "";
        for (int j = 0; j < sc.Count; j++)
        {
            String LenghtStr = "&nbsp;";
            string[] aa = sc[j].ToString().Split(new char[] { '※' });
            if (!scKey.Contains(aa[0]))
            {
                scKey.Add(aa[0]);
                o = 1;
            }
            else
            {
                o += 1;
            }

            if (no % 2 == 0)
            {
                style = "class='GridViewRowStyle'";
            }
            else
            {
                style = "class='GridViewAlternatingRowStyle'";
            }
            //if (aa[1] == "1")
            //{
            //    sb.Append("<tr " + style + " Style='background-color: #FFFF00;'>\n");
            //}
            //else
            //{
            //    sb.Append("<tr " + style + ">\n");
            //}
            sb.Append("<tr " + style + ">\n");
            sb.Append("<td  align='center'>");
            sb.Append(aa[0] + "--" + o.ToString());
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append(aa[2]);
            sb.Append("</td>\n");
            sb.Append("<td  width='30%'>");
            sb.Append(aa[3]);
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td  width='40%'>");//計畫範圍
            sb.Append(aa[4]);
            sb.Append("</td>\n");
            sb.Append("<td   >");
            sb.Append(aa[5]);
            sb.Append("</td>\n");
            sb.Append("<td  width='50%'>");
            sb.Append(aa[6]);
            sb.Append("</td>\n");
            if (aa[7].Trim() != "&nbsp;" && aa[8].Trim() != "&nbsp;")
            {
                LenghtStr = aa[7].Trim() + "~" + aa[8].Trim();
            }
            sb.Append("<td  >");
            sb.Append(LenghtStr);
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append(aa[9]);
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append(aa[10]);
            sb.Append("</td>\n");
            sb.Append("<td  >");
            sb.Append(aa[11]);
            sb.Append("</td>\n");
            sb.Append("<td  >&nbsp;");
            sb.Append(aa[12]);
            sb.Append("</td>\n");
            /*
            sb.Append("<td style=\"border-color : Black;border-style : solid;border-top-width :0mm;border-right-width : 0.3mm;border-left-width : 0.3mm;border-bottom-width : 0.3mm;\" class=\"Noprint\" >");
            if (aa[13].Trim() != "")
            {
                sb.Append("<img onClick=\"OpenPlan('" + aa[13].Trim() + "','" + species + "');\" onMouseOver=\"this.style.cursor='hand'\" src=\"image/deep.gif\" width=\"22\" height=\"16\" border=0>");
            }
            else
            {
                sb.Append("&nbsp;");
            }
            sb.Append("</td>\n");
            */
            sb.Append("</tr>\n");
            //myrowNo += 1;
            no += 1;
        }
        sb.Append("</table>\n");
        //----------------------------------------


        #endregion
        return sb;
    }
    public StringBuilder Report2(StringCollection sc)
    {
        StringBuilder sb = new StringBuilder();
        #region 表尾合計

        int CountRow1 = 0;
        int CountRow2 = 0;
        int CountRow3 = 0;
        int CountRow4 = 0;
        int CountRow5 = 0;
        int CountRow6 = 0;
        int CountRow7 = 0;
        int CountRow8 = 0;
        int CountRow9 = 0;

        #endregion


        #region 表頭
        //sb.Append("<table width='100%'>\n");

        sb.Append("<table class=\"GridViewStyle\"  rules=\"all\" id='TABLE1' border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width='100%'>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<td class=\"tabmidb\" colspan='13' width='100%' align='center'>");
        sb.Append((int.Parse(ddl_year.SelectedValue) - 1911).ToString() + " 年計畫性挖掘初步整合會議資料表(未互相重疊案件)---D表</td>");
        sb.Append("</tr>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<td  align='center'>項目</td>");
        sb.Append("<td  align='center'>申請編號</td>");
        sb.Append("<td  align='center'>申請/協辦單位</td>");
        sb.Append("<td  align='center'>主</td>");
        sb.Append("<td  align='center'>從</td>");
        sb.Append("<td  align='center'>計畫名稱</td>");
        sb.Append("<td  align='center'>行政區</td>");
        sb.Append("<td  align='center'>計畫範圍</td>");
        sb.Append("<td  align='center'>預定工期</td>");
        sb.Append("<td  align='center'>挖掘長度</td>");
        sb.Append("<td  align='center'>最遲送件時程</td>");
        sb.Append("<td  align='center'>協調應辦事項</td>");
        sb.Append("<td align='center'>整合編號</td>");
        sb.Append("</tr>");

        #endregion

        StringCollection scKey = new StringCollection();
        #region 內容
        //-------------------------------------------------------
        int o = 1;
        int no = 1;
        string style = "";
        for (int j = 0; j < sc.Count; j++)
        {
            String LenghtStr = "&nbsp;";
            string[] aa = sc[j].ToString().Split(new char[] { '※' });
            if (!scKey.Contains(aa[0]))
            {
                scKey.Add(aa[0]);
                o = 1;
            }
            else
            {
                o += 1;
            }
            if (no % 2 == 0)
            {
                style = "class='GridViewRowStyle'";
            }
            else
            {
                style = "class='GridViewAlternatingRowStyle'";
            }
            //if (aa[1] == "1")
            //{
            //    sb.Append("<tr " + style + " Style='background-color: #FFFF00;'>\n");
            //}
            //else
            //{
            //    sb.Append("<tr " + style + ">\n");
            //}
            sb.Append("<tr " + style + ">\n");
            sb.Append("<td width='70' align='center'>");
            sb.Append(aa[0]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[2]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[3]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[4]);
            sb.Append("</td>\n");
            sb.Append("<td width='90' >");
            sb.Append(aa[5]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[6]);
            sb.Append("</td>\n");
            if (aa[7].Trim() != "&nbsp;" && aa[8].Trim() != "&nbsp;")
            {
                LenghtStr = aa[7].Trim() + "~" + aa[8].Trim();
            }
            sb.Append("<td >");
            sb.Append(LenghtStr);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[9]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[10]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[11]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[12]);
            sb.Append("</td>\n");
            sb.Append("</tr>\n");
            //myrowNo += 1;
            no += 1;
        }
        sb.Append("</table>\n");
        //----------------------------------------
        #endregion
        return sb;
    }
    public StringBuilder Report3(StringCollection sc)
    {
        StringBuilder sb = new StringBuilder();
        #region 表尾合計

        int CountRow1 = 0;
        int CountRow2 = 0;
        int CountRow3 = 0;
        int CountRow4 = 0;
        int CountRow5 = 0;
        int CountRow6 = 0;
        int CountRow7 = 0;
        int CountRow8 = 0;
        int CountRow9 = 0;

        #endregion


        #region 表頭
        //sb.Append("<table width='100%'>\n");
        sb.Append("<table class=\"GridViewStyle\"  rules=\"all\" id='TABLE1' border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width='100%'>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<td class=\"tabmidb\" colspan='14' width='100%' align='center'>");
        sb.Append((int.Parse(ddl_year.SelectedValue) - 1911).ToString() + " 年計畫性挖掘初步整合會議資料表</td>");
        sb.Append("</tr>");
        sb.Append("<tr class=\"GridViewHeaderStyle\">");
        sb.Append("<td  align='center'>項目</td>");
        sb.Append("<td  align='center'>申請編號</td>");
        sb.Append("<td  align='center'>申請/協辦單位</td>");
        sb.Append("<td  align='center'>主</td>");
        sb.Append("<td  align='center'>從</td>");
        sb.Append("<td  align='center'>計畫名稱</td>");
        sb.Append("<td  align='center'>行政區</td>");
        sb.Append("<td  align='center'>計畫範圍</td>");
        sb.Append("<td  align='center'>預定工期</td>");
        sb.Append("<td  align='center'>挖掘長度</td>");
        sb.Append("<td  align='center'>最遲送件時程</td>");
        sb.Append("<td  align='center'>協調應辦事項</td>");
        sb.Append("<td  align='center'>整合編號</td>");
        //sb.Append("<td  align='center'>位置圖</td>");
        sb.Append("</tr>");

        #endregion

        StringCollection scKey = new StringCollection();
        #region 內容
        //-------------------------------------------------------
        int o = 1;
        int no = 1;
        string style = "";
        
        for (int j = 0; j < sc.Count; j++)
        {
            String LenghtStr = "&nbsp;";
            string[] aa = sc[j].ToString().Split(new char[] { '※' });
            if (!scKey.Contains(aa[0]))
            {
                scKey.Add(aa[0]);
                o = 1;
            }
            else
            {
                o += 1;
            }
            if (no % 2 == 0)
            {
                style = "class='GridViewRowStyle'";
            }
            else
            {
                style = "class='GridViewAlternatingRowStyle'";
            }
            //if (aa[1] == "1")
            //{
            //    sb.Append("<tr " + style + " Style='background-color: #FFFF00;'>\n");
            //}
            //else
            //{
            //    sb.Append("<tr " + style + ">\n");
            //}
            sb.Append("<tr " + style + ">\n");
            sb.Append("<td width='70' >");
            //項目
            sb.Append(no.ToString());
            sb.Append("</td>\n");
            sb.Append("<td >");
            //申請編號
            sb.Append(aa[2]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            //申請/協辦單位
            sb.Append(aa[3]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append("&nbsp;");
            sb.Append("</td>\n");
            sb.Append("<td >");
            //計畫名稱
            sb.Append(aa[4]);
            sb.Append("</td>\n");
            sb.Append("<td width='90' >");
            //行政區
            sb.Append(aa[5]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            //計畫範圍
            sb.Append(aa[6]);
            sb.Append("</td>\n");
            //預定工期
            if (aa[7].Trim() != "&nbsp;" && aa[8].Trim() != "&nbsp;")
            {
                LenghtStr = aa[7].Trim() + "~" + aa[8].Trim();
            }
            sb.Append("<td >");
            sb.Append(LenghtStr);
            sb.Append("</td>\n");
            sb.Append("<td >");
            //挖掘長度
            sb.Append(aa[9]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[10]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            sb.Append(aa[11]);
            sb.Append("</td>\n");
            sb.Append("<td >");
            //整合編號
            sb.Append(aa[12]);
            sb.Append("</td>\n");
            /*
            sb.Append("<td>");            
            if (aa[14].Trim() != "")
            {
                //sb.Append("<img onClick=\"OpenPlan('" + aa[14].Trim() + "','');\" onMouseOver=\"this.style.cursor='hand'\" src=\"image/deep.gif\" width=\"22\" height=\"16\" border=0>");
                sb.Append("<a href=javascript:golatLng2(" + aa[14].Trim() + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>");
            }
            else
            {
                sb.Append("&nbsp;");
            }
            
            sb.Append("</td>\n");            
            */
            sb.Append("</tr>\n");            
            //myrowNo += 1;
            no += 1;
        }
        sb.Append("</table>\n");
        //----------------------------------------
        #endregion
        return sb;
    }
    #endregion

    #region ----------------BindGrid(GW)-------------------
    protected void BindGrid(AspNetPager AspNetPager_, GridView GVList)
    {
        //DataTable dt = new DataTable();
        //dt = getData();
        DataSet dt = new DataSet();
        dt = getData2();
        AspNetPager_.RecordCount = getDataCount();
        //AspNetPager_.RecordCount = dt.Rows.Count;

        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Tables[0].Rows.Count > 0)
        {
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
            //Button3.Visible = true;
            GridView3.Visible = true;
        }
    }
    //一般案件總數
    private int getDataCount()
    {
        string strCmd = "";
        int cou = 0;
        string sql1 = "";
        string sql4 = "";
        string sql5 = "", sql6 = "", sql6_1 = "", sql6_2 = "", sql6_3 = "";
        //sql1 = sql1 + " and dig_st>='" + DateTime.Now.ToShortDateString() + " 00:00:00" + "' and dig_et<='" + DateTime.Now.ToShortDateString() + " 23:59:59" + "' ";
        string sdt = DateTime.Now.ToShortDateString() + " 00:00:00";
        string edt = DateTime.Now.ToShortDateString() + " 23:59:59";
        sql1 = sql1 + " and ((dig_st>='" + sdt + "' and dig_et<='" + edt + "') or (dig_st<='" + sdt + "' and  dig_et<'" + edt + "' and dig_et>='" + sdt + "') " +
                         "or (dig_st>='" + sdt + "' and dig_st<'" + edt + "' and dig_et>='" + edt + "') or (dig_st<'" + sdt + "' and dig_et>='" + sdt + "' and dig_et<='" + sdt + "') " +
                         "or (dig_st<'" + sdt + "' and dig_et>'" + edt + "')) ";
        //地址-一般案件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
            //sql4 = " and b.construction like '%" + SQLInJect(tb_pos.Text) + "%' ";
            //sql4 = " and b.WorkSN like '%" + SQLInJect(tb_pos.Text) + "%' ";
            //sql4 = " AND (b.TargetLBName like '%" + SQLInJect(tb_pos.Text).Trim() + "%' or b.UnitName like '%" + SQLInJect(tb_pos.Text).Trim() + "%' or b.WorkSN like '%" + SQLInJect(tb_pos.Text).Trim() + "%')";
            sql6 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or ppcodeName like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_1 = " and (b.WorkSN like '%" + SQLInJect(tb_pos.Text) + "%' or PIPE_CMP_1.PLINE_CMP_ABBR like '%" + SQLInJect(tb_pos.Text) + "%' or b.TargetLBName like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_2 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_3 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
        }
        //地址-緊急案件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
            //sql5 = " and postion like '%" + SQLInJect(tb_pos.Text) + "%' ";
            //sql5 = " and (postion like '%" + SQLInJect(tb_pos.Text).Trim() + "%' or area like '%" + SQLInJect(tb_pos.Text).Trim() + "%' or PLINE_CMP_ABBR like '%" + SQLInJect(tb_pos.Text).Trim() + "%')";
        }
        //strCmd = "select COUNT(*) cou from " +
        //         //" (select a.keytime from Pipe_UsuallyCaseSame a,View_CaseBasic b where 1=1 and (b.LicNo like '%a.licenses%' or b.caseid=a.caseid)" + sql1 + sql4 +
        //         " (select a.keytime from dbo.Pipe_UsuallyCaseSame AS a INNER JOIN dbo.View_CaseBasic AS b ON a.caseid = b.CaseID where 1=1 " + sql1 + sql4 +
        //         " union all" +
        //         //" select keytime from Pipe_UsuallyCaseUrgent where 1=1 " + sql1 + sql5 + ") a;";
        //         " select keytime from Pipe_UsuallyCaseUrgent left join usermanager on Pipe_UsuallyCaseUrgent.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_UsuallyCaseUrgent.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql5 +
        //        " union all" +
        //        " select keytime from Pipe_SelfInspections left join usermanager on Pipe_SelfInspections.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_SelfInspections.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql5 + ") a;";
        //        //Response.Write(strCmd); Response.End();
        strCmd = "select COUNT(*) cou from " +
                 "( " +
                  "select b.TargetLBName area " +
                  " from dbo.Pipe_UsuallyCaseSame AS a INNER JOIN dbo.View_CaseBasic AS b ON a.caseid = b.CaseID INNER JOIN dbo.PIPE_CMP AS PIPE_CMP_1 ON a.ppcode = PIPE_CMP_1.PLINE_CMP_NO INNER JOIN dbo.USERMANAGER AS USERMANAGER_1 ON a.userid = USERMANAGER_1.Emp_Login where 1=1 " +
                   sql1 + sql6_1 + //sql4 +
                  " union all " +
                  " select area num " +
                  " from Pipe_UsuallyCaseUrgent left join usermanager on Pipe_UsuallyCaseUrgent.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_UsuallyCaseUrgent.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_2 + //+ sql5;
                    " union all " +
                    " select area num " +
                    " from Pipe_SelfInspections left join usermanager on Pipe_SelfInspections.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_SelfInspections.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_3 +  //+ sql5;
                ") bb;";
        //Response.Write(strCmd+"<br>");
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader dr = Sqlcmd.ExecuteReader())
                    {
                        if (dr != null)
                        {
                            if (dr.Read())
                            {
                                cou = int.Parse(dr["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        //SqlDataReader dr = ProjectClass.getDataReader(strCmd, "1");
        //if (dr != null)
        //{
        //    if (dr.Read())
        //    {
        //        cou = int.Parse(dr["cou"].ToString());
        //        dr.Close();
        //        dr.Dispose();
        //    }


        //}
        //else
        //{
        //    cou = 0;
        //}
        return cou;
    }
   
    // 2020.02.10 調整SQL查詢條件, 比對便民系統今日施工案件條件, 避免首頁與便民系統筆數不一致
    private DataSet getData2()
    {
        //Response.Write("getData2");
        string sqlstr = "",
               sqlUsuallyCase = "", // 一般案件
               sqlUrgenCase = "", // 搶修
               sqlSelfInspection = "", // 缺失;
               //dateStr = DateTime.Now.ToShortDateString() + " 00:00:00",
               //dateStr = "2020/2/5" + " 00:00:00",
               sqlDateCondition = " (CONVERT(date, getDate()) between convert(DATE, dig_st) and convert(DATE, dig_et) or CONVERT(date, getDate()) = convert(DATE, dig_st))",
               sqlUsuallyCaseQueryCondition = "", 
               sqlUrgenCaseQueryCondition = "", 
               sqlSelfInspectionQueryCondtition = "";

        // 頁面查詢條件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
            sqlUsuallyCaseQueryCondition = " and (b.WorkSN like '%" + SQLInJect(tb_pos.Text) + "%' or PIPE_CMP_1.PLINE_CMP_ABBR like '%" + SQLInJect(tb_pos.Text) + "%' or b.TargetLBName like '%" + SQLInJect(tb_pos.Text) + "%')";
            sqlUrgenCaseQueryCondition = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%') ";
            sqlSelfInspectionQueryCondtition = sqlUrgenCaseQueryCondition;
        }

        // 一般案件
        sqlUsuallyCase =
        @"select nos,
                 b.TargetLBName AS area,
                 licenses,
                 dig_st,
                 dig_et,
                 ppcode,
                 a.userid,
                 b.WorkSN AS postion,
                 keytime,
                 '一般' [type],
                 PIPE_CMP_1.PLINE_CMP_ABBR AS ppcodeName,
                 USERMANAGER_1.Emp_Name AS userName, 
                 '' Tar_l,
                 '' Tar_w,
                 '' sidewalk_l,
                 '' sidewalk_w,
                 '' lid,'' other,
                 b.ConstName as labTemp,
                 b.caseid, 
                 b.RoadType as RoadType0,
                 convert(varchar,b.[Length]) as Length0,
                 convert(varchar,b.Width) as Width0,
                 convert(varchar,b.Depth) as Depth0,
                 convert(varchar,b.Point) as Point0,
                 convert(varchar,b.Area) as Area0,
                 b.RoadType1,convert(varchar,b.Length1) as Length1,
                 convert(varchar,b.Width1) as Width1,
                 convert(varchar,b.Depth1) as Depth1,
                 convert(varchar,b.Point1) as Point1,
                 convert(varchar,b.Area1) as Area1,
                 b.RoadType2,
                 convert(varchar,b.Length2) as Length2,
                 convert(varchar,b.Width2) as Width2,
                 convert(varchar,b.Depth2) as Depth2,
                 convert(varchar,b.Point2) as Point2,
                 convert(varchar,b.Area2) as Area2,
                 '' lon,
                 '' lat,
                 (convert(varchar,Supervise) + case when Supervise_Tel<>'' or Supervise_Tel is not null then case when Substring(Rtrim(Ltrim(Supervise_Tel)),1,2)<>'09' then CHAR(13) + convert(varchar,Supervise_Tel) else '' end end ) as mySupervise, 
                 (convert(varchar,Factory) + case when Factory_Man_Tel<>'' or Factory_Man_Tel is not null then case when Substring(Rtrim(Ltrim(Factory_Man_Tel)),1,2)<>'09' then CHAR(13) + convert(varchar,Factory_Man_Tel) else '' end end )  as myFactory 
            from (select ROW_NUMBER() over (Partition by caseid order by Caseid) as Rnum,* 
                    from dbo.Pipe_UsuallyCaseSame 
                   where (CONVERT(date, getDate()) between CONVERT(date,dig_st) and CONVERT(date,dig_et) or CONVERT(date, getDate()) = CONVERT(date,dig_st)) ) AS a 
            JOIN dbo.View_CaseBasic AS b 
              ON a.caseid = b.CaseID 
             and a.Rnum=1 INNER 
            JOIN dbo.PIPE_CMP AS PIPE_CMP_1 
              ON a.ppcode = PIPE_CMP_1.PLINE_CMP_NO 
            JOIN dbo.USERMANAGER AS USERMANAGER_1
              ON a.userid = USERMANAGER_1.Emp_Login
           where " + sqlDateCondition + // 時間條件
                     sqlUsuallyCaseQueryCondition; // 查詢條件
                 
        // 搶修
        sqlUrgenCase =
        @"select nos,
                 area,
                 licenses,
                 dig_st,
                 dig_et,
                 ppcode,
                 usermanager.userid,
                 postion,
                 keytime,
                 '緊急' [type],
                 pipe_cmp.[PLINE_CMP_ABBR] ppcodeName,
                 usermanager.Emp_name userName, 
                 Tar_l,
                 Tar_w,
                 sidewalk_l,
                 sidewalk_w,
                 lid,other,
                 '' labTemp,
                 '' caseid,
                 '' RoadType0,
                 '' Length0,
                 '' Width0,
                 '' Depth0,
                 '' Point0,
                 '' Area0,
                 '' RoadType1,
                 '' Length1,
                 '' Width1,
                 '' Depth1,
                 '' Point1,
                 '' Area1,
                 '' RoadType2,
                 '' Length2,
                 '' Width2,
                 '' Depth2,
                 '' Point2,
                 '' Area2,
                 lon,
                 lat,
                 (convert(varchar,emercont) + case when tel<>'' or tel is not null then case when Substring(Rtrim(Ltrim(tel)),1,2)<>'09' then CHAR(13) + convert(varchar,tel) else '' end end) mySupervise,
                 '' myFactory 
            from Pipe_UsuallyCaseUrgent 
       left join usermanager 
              on Pipe_UsuallyCaseUrgent.userid = usermanager.Emp_Login  
       left join pipe_cmp 
              on Pipe_UsuallyCaseUrgent.ppcode = pipe_cmp.PLINE_CMP_NO 
           where " + sqlDateCondition + // 時間條件
                     sqlUrgenCaseQueryCondition ; // 查詢條件

         // 缺失
        sqlSelfInspection = 
        @"select nos,
                 area,
                 licenses,
                 dig_st,
                 dig_et,
                 ppcode,
                 usermanager.userid,
                 postion,
                 keytime,
                 '缺失' [type],
                 pipe_cmp.[PLINE_CMP_ABBR] ppcodeName,
                 usermanager.Emp_name userName, 
                 Tar_l,
                 Tar_w,
                 sidewalk_l,
                 sidewalk_w,
                 lid,other,
                 '' labTemp,
                 '' caseid,
                 '' RoadType0,
                 '' Length0,
                 '' Width0,
                 '' Depth0,
                 '' Point0,
                 '' Area0,
                 '' RoadType1,
                 '' Length1,
                 '' Width1,
                 '' Depth1,
                 '' Point1,
                 '' Area1,
                 '' RoadType2,
                 '' Length2,
                 '' Width2,
                 '' Depth2,
                 '' Point2,
                 '' Area2,
                 lon,
                 lat,
                 (convert(varchar,emercont) + case when tel<>'' or tel is not null then case when Substring(Rtrim(Ltrim(tel)),1,2)<>'09' then CHAR(13) + convert(varchar,tel) else '' end end) mySupervise,
                 '' myFactory 
            from Pipe_SelfInspections 
       left join usermanager 
              on Pipe_SelfInspections.userid = usermanager.Emp_Login  
       left join pipe_cmp 
              on Pipe_SelfInspections.ppcode = pipe_cmp.PLINE_CMP_NO 
           where " + sqlDateCondition + //日期條件
                     sqlSelfInspectionQueryCondtition + // 查詢條件
           @"and (select count(*) 
                    from AppUploadPic 
                   where Pic_No in (select Up_No 
                                      from AppUpload 
                                     where Upload_Item = 'R') 
                     and Pic_Type in (36,37,38,39) 
                     and AppUploadPic.Pic_ID = Pipe_SelfInspections.AppUploadID)>=0  
             and ((select count(*) 
                     from MISSINGCASE_PIC a
                     join MISSINGCASE_PIC b 
                       on a.Up_No = b.Up_No
                     join MISSINGCASE_PIC c 
                       on a.Up_No = c.Up_No
                     join MISSINGCASE_PIC d 
                       on a.Up_No = d.Up_No
                    where a.Up_No = Pipe_SelfInspections.AppUploadID
                      and a.FileName LIKE '%MissingPic3%'
                      and b.FileName LIKE '%MissingPic4%'
                      and c.FileName LIKE '%MissingPic5%'
                      and d.FileName LIKE '%MissingPic6%') > 0
		          or     
                  (select count(*) 
                     from ViolationCase_PIC a
                     join ViolationCase_PIC b 
                       on a.Up_No = b.Up_No
                     join ViolationCase_PIC c 
                       on a.Up_No = c.Up_No
                     join ViolationCase_PIC d 
                       on a.Up_No = d.Up_No
                    where a.Up_No = Pipe_SelfInspections.AppUploadID
                      and a.FileName LIKE '%ViolationPic3%'
                      and b.FileName LIKE '%ViolationPic4%'
                      and c.FileName LIKE '%ViolationPic5%'
                      and d.FileName LIKE '%ViolationPic6%') > 0)";
        
        //Response.Write(sqlUsuallyCase + "<br/>");
        //Response.Write(sqlUrgenCase + "<br/>");
        //Response.Write(sqlSelfInspection + "<br/>");

        sqlstr = sqlUsuallyCase + // 一般案件
                 " union all " + 
                 sqlUrgenCase + // 搶修
                 " union all " +
                 sqlSelfInspection; // 缺失
        
        string strSQL_Order = " ORDER BY area";
        string sqlFormat = string.Format(
           "SELECT * FROM (SELECT  " +
           "* FROM ({0}) B)C {1} ;",
           sqlstr,
           strSQL_Order);

        DataSet dtt = SqlHelper.ExecuteDataset(SqlHelper.ConnectionString, CommandType.Text, sqlFormat);
        GC.Collect();
        return dtt;
    }


    private DataTable getDatatot()
    {
        string sqlstr = "";
        string sql1 = "";
        string sql4 = "";
        string sql5 = "", sql6_1 = "", sql6_2 = "", sql6_3 = "";
        string sdt = DateTime.Now.ToShortDateString() + " 00:00:00";
        string edt = DateTime.Now.ToShortDateString() + " 23:59:59";
        sql1 = sql1 + " and ((dig_st>='" + sdt + "' and dig_et<='" + edt + "') or (dig_st<='" + sdt + "' and  dig_et<'" + edt + "' and dig_et>='" + sdt + "') " +
                         "or (dig_st>='" + sdt + "' and dig_st<'" + edt + "' and dig_et>='" + edt + "') or (dig_st<'" + sdt + "' and dig_et>='" + sdt + "' and dig_et<='" + sdt + "') " +
                         "or (dig_st<'" + sdt + "' and dig_et>'" + edt + "')) ";
        //地址-一般案件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
            sql6_1 = " and (b.WorkSN like '%" + SQLInJect(tb_pos.Text) + "%' or PIPE_CMP_1.PLINE_CMP_ABBR like '%" + SQLInJect(tb_pos.Text) + "%' or b.TargetLBName like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_2 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_3 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
        }
        //地址-緊急案件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
        }

        sqlstr = "select area,SUM(num) num from " +
                 "( " +
                  "select area,COUNT(*) num from ( " +
                  "select b.TargetLBName area,COUNT(*) num,b.WorkSN  " +
                  " from dbo.Pipe_UsuallyCaseSame AS a INNER JOIN dbo.View_CaseBasic AS b ON a.caseid = b.CaseID INNER JOIN dbo.PIPE_CMP AS PIPE_CMP_1 ON a.ppcode = PIPE_CMP_1.PLINE_CMP_NO INNER JOIN dbo.USERMANAGER AS USERMANAGER_1 ON a.userid = USERMANAGER_1.Emp_Login where 1=1 " +
                   sql1 + sql6_1 + //sql4 +
                  "group by b.WorkSN,b.TargetLBName " +
                  ") c group by c.area " +
                  " union all " +
                  " select area,COUNT(*) num " +
                  " from Pipe_UsuallyCaseUrgent left join usermanager on Pipe_UsuallyCaseUrgent.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_UsuallyCaseUrgent.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_2 + //+ sql5;
                  " group by area " +
                    " union all " +
                    " select area,COUNT(*) num " +
                    " from Pipe_SelfInspections left join usermanager on Pipe_SelfInspections.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_SelfInspections.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_3 + 
										" and (select count(*) from AppUploadPic where Pic_No in (select Up_No from AppUpload where Upload_Item = 'R') and Pic_Type in (36,37) and AppUploadPic.Pic_ID=Pipe_SelfInspections.AppUploadID)>=2 " +
                  	" and ((select count(*) from MISSINGCASE_PIC where MISSINGCASE_PIC.Up_No=Pipe_SelfInspections.AppUploadID and (FileName like '%MissingPic3%' or FileName like '%MissingPic4%'))>=2 " +
                  	"				or (select count(*) from ViolationCase_PIC where ViolationCase_PIC.Up_No=Pipe_SelfInspections.AppUploadID and (FileName like '%ViolationPic3%' or FileName like '%ViolationPic4%'))>=2) " +
                    " group by area " + 
                    ") bb" +
                   " group by area order by area;";
	
        //Response.Write(sqlstr + "<br>");
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {
                
                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
    }

    //一般案件查詢
    protected void btn0_Click(object sender, EventArgs e)
    {
        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();
        AspNetPager_Result_0.RecordCount = ApplyListInfo.GetApplyResultCount(Dist[0], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", SQLInJect(tb_0.Text));
        BindGrid_Result(Dist[0], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", this.AspNetPager_Result_0, this.GVList_Result_0, SQLInJect(tb_0.Text));
    }

    //查詢
    protected void Button2_Click(object sender, EventArgs e)
    {
        
        #region-------區域統計---------------
        DataTable dt = new DataTable();
        for (int i = 0; i < 6; i++)
            dt.Columns.Add(i.ToString());

        DataTable dta = getDatatot();
        int tot = 0;
        for (int i = 0; i < 37; i++)
        {
            for (int j = 0; j < dta.Rows.Count; j++)
            {
                if (areas[i] == dta.Rows[j][0].ToString())
                {
                    areaint[i] = int.Parse(dta.Rows[j][1].ToString());
                    tot = tot + int.Parse(dta.Rows[j][1].ToString());
                }
            }
        }
        dt.Rows.Add(areas[0] + "(" + areaint[0].ToString() + ")", areas[1] + "(" + areaint[1].ToString() + ")", areas[2] + "(" + areaint[2].ToString() + ")", areas[3] + "(" + areaint[3].ToString() + ")", areas[4] + "(" + areaint[4].ToString() + ")", areas[5] + "(" + areaint[5].ToString() + ")");
        dt.Rows.Add(areas[6] + "(" + areaint[6].ToString() + ")", areas[7] + "(" + areaint[7].ToString() + ")", areas[8] + "(" + areaint[8].ToString() + ")", areas[9] + "(" + areaint[9].ToString() + ")", areas[10] + "(" + areaint[10].ToString() + ")", areas[11] + "(" + areaint[11].ToString() + ")");
        dt.Rows.Add(areas[12] + "(" + areaint[12].ToString() + ")", areas[13] + "(" + areaint[13].ToString() + ")", areas[14] + "(" + areaint[14].ToString() + ")", areas[15] + "(" + areaint[15].ToString() + ")", areas[16] + "(" + areaint[16].ToString() + ")", areas[17] + "(" + areaint[17].ToString() + ")");
        dt.Rows.Add(areas[18] + "(" + areaint[18].ToString() + ")", areas[19] + "(" + areaint[19].ToString() + ")", areas[20] + "(" + areaint[20].ToString() + ")", areas[21] + "(" + areaint[21].ToString() + ")", areas[22] + "(" + areaint[22].ToString() + ")", areas[23] + "(" + areaint[23].ToString() + ")");
        dt.Rows.Add(areas[25] + "(" + areaint[25].ToString() + ")", areas[26] + "(" + areaint[26].ToString() + ")", areas[27] + "(" + areaint[27].ToString() + ")", areas[28] + "(" + areaint[28].ToString() + ")", areas[29] + "(" + areaint[29].ToString() + ")", areas[30] + "(" + areaint[30].ToString() + ")");
        dt.Rows.Add(areas[31] + "(" + areaint[31].ToString() + ")", areas[32] + "(" + areaint[32].ToString() + ")", areas[33] + "(" + areaint[33].ToString() + ")", areas[34] + "(" + areaint[34].ToString() + ")", areas[35] + "(" + areaint[35].ToString() + ")", areas[36] + "(" + areaint[36].ToString() + ")");
        dt.Rows.Add(areas[24] + "(" + areaint[24].ToString() + ")", "", "", "", "", "");
        Label16.Text = tot.ToString();
        this.GridView3.DataSource = dt;
        this.GridView3.DataBind();
        #endregion
        BindGrid(this.AspNetPager_Result_5, this.GridView0);
    }
    #region ----------------GridView0_RowDataBound()-------------------
    protected void GridView0_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            Label Lab_nos = (Label)e.Row.FindControl("Lab_nos");
            Label lab_postion = (Label)e.Row.FindControl("lab_postion");

            #region-------------施工位置----------------
            Literal Literal_Map = (Literal)e.Row.FindControl("Literal_Map");
            Label Label_X = (Label)e.Row.FindControl("lab_X");
            Label Label_Y = (Label)e.Row.FindControl("lab_Y");
            string lat = DataBinder.Eval(e.Row.DataItem, "lat").ToString();
            string lon = DataBinder.Eval(e.Row.DataItem, "lon").ToString();
            string caseid = DataBinder.Eval(e.Row.DataItem, "Caseid").ToString() != "0" ? DataBinder.Eval(e.Row.DataItem, "Caseid").ToString() : "";
            if (lat != "")
            {
                Literal_Map.Text = "<a href=javascript:golatLng2(" + lat + "," + lon + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";
            }
            else
            {
                Literal_Map.Text = "<a href=javascript:initialize('','','','" + caseid + "'); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";
            }
            Literal_Map.Visible = true;
            Label_X.Visible = false;
            Label_Y.Visible = false;


            #endregion

            #region 工作內容
            String RoadTypeStr = "";
            if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "RoadType0").ToString()) && !string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length0").ToString()))
            {
                switch (DataBinder.Eval(e.Row.DataItem, "RoadType0").ToString())
                {
                    case "0":
                        RoadTypeStr = RoadTypeStr + "柏油";
                        break;
                    case "1":
                        RoadTypeStr = RoadTypeStr + "混凝土";
                        break;
                    case "2":
                        RoadTypeStr = RoadTypeStr + "碎石子";
                        break;
                    case "3":
                        RoadTypeStr = RoadTypeStr + "紅磚";
                        break;
                    case "4":
                        RoadTypeStr = RoadTypeStr + "其它";
                        break;
                    case "5":
                        RoadTypeStr = RoadTypeStr + "土路面";
                        break;
                    default:
                        break;
                }

                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length0").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "(長" + DataBinder.Eval(e.Row.DataItem, "Length0").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Width0").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",寬" + DataBinder.Eval(e.Row.DataItem, "Width0").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Depth0").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",深" + DataBinder.Eval(e.Row.DataItem, "Depth0").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Point0").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "," + DataBinder.Eval(e.Row.DataItem, "Point0").ToString() + "處";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Area0").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",面積" + DataBinder.Eval(e.Row.DataItem, "Area0").ToString() + "平方公尺)";
                }
            }
            if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "RoadType1").ToString()) && !string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length1").ToString()))
            {
                switch (DataBinder.Eval(e.Row.DataItem, "RoadType1").ToString())
                {
                    case "0":
                        RoadTypeStr = RoadTypeStr + "柏油";
                        break;
                    case "1":
                        RoadTypeStr = RoadTypeStr + "混凝土";
                        break;
                    case "2":
                        RoadTypeStr = RoadTypeStr + "碎石子";
                        break;
                    case "3":
                        RoadTypeStr = RoadTypeStr + "紅磚";
                        break;
                    case "4":
                        RoadTypeStr = RoadTypeStr + "其它";
                        break;
                    case "5":
                        RoadTypeStr = RoadTypeStr + "土路面";
                        break;
                    default:
                        break;
                }

                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length1").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "(長" + DataBinder.Eval(e.Row.DataItem, "Length1").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Width1").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",寬" + DataBinder.Eval(e.Row.DataItem, "Width1").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Depth1").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",深" + DataBinder.Eval(e.Row.DataItem, "Depth1").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Point1").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "," + DataBinder.Eval(e.Row.DataItem, "Point1").ToString() + "處";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Area1").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",面積" + DataBinder.Eval(e.Row.DataItem, "Area1").ToString() + "平方公尺)";
                }
            }
            if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "RoadType2").ToString()) && !string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length2").ToString()))
            {
                switch (DataBinder.Eval(e.Row.DataItem, "RoadType2").ToString())
                {
                    case "0":
                        RoadTypeStr = RoadTypeStr + "柏油";
                        break;
                    case "1":
                        RoadTypeStr = RoadTypeStr + "混凝土";
                        break;
                    case "2":
                        RoadTypeStr = RoadTypeStr + "碎石子";
                        break;
                    case "3":
                        RoadTypeStr = RoadTypeStr + "紅磚";
                        break;
                    case "4":
                        RoadTypeStr = RoadTypeStr + "其它";
                        break;
                    case "5":
                        RoadTypeStr = RoadTypeStr + "土路面";
                        break;
                    default:
                        break;
                }

                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Length2").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "(長" + DataBinder.Eval(e.Row.DataItem, "Length2").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Width2").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",寬" + DataBinder.Eval(e.Row.DataItem, "Width2").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Depth2").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",深" + DataBinder.Eval(e.Row.DataItem, "Depth2").ToString() + "公尺";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Point2").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + "," + DataBinder.Eval(e.Row.DataItem, "Point2").ToString() + "處";
                }
                if (!string.IsNullOrEmpty(DataBinder.Eval(e.Row.DataItem, "Area2").ToString()))
                {
                    RoadTypeStr = RoadTypeStr + ",面積" + DataBinder.Eval(e.Row.DataItem, "Area2").ToString() + "平方公尺)";
                }
            }

            Label lab_Tar_l = (Label)e.Row.FindControl("lab_Tar_l");
            Label lab_Tar_w = (Label)e.Row.FindControl("lab_Tar_w");
            Label lab_sidewalk_l = (Label)e.Row.FindControl("lab_sidewalk_l");
            Label lab_sidewalk_w = (Label)e.Row.FindControl("lab_sidewalk_w");
            Label lab_lid = (Label)e.Row.FindControl("lab_lid");
            Label lab_other = (Label)e.Row.FindControl("lab_other");
            Label lab_txt = (Label)e.Row.FindControl("lab_txt");
            string Tar = "柏油挖掘 長(m):";
            string sidewalk = "人行道挖掘 長(m):";
            string lid = "孔蓋升降:";
            string other = "其他:";
            string res = "";
            if (lab_Tar_l.Text != "" && lab_Tar_w.Text != "")
                res = Tar + lab_Tar_l.Text + " ,寬(m):" + lab_Tar_w.Text + "<br>";
            if (lab_sidewalk_l.Text != "" && lab_sidewalk_w.Text != "")
                res = res + sidewalk + lab_sidewalk_l.Text + " ,寬(m):" + lab_sidewalk_w.Text + "<br>";
            if (lab_lid.Text != "")
                res = res + lid + lab_lid.Text + "處" + "<br>";
            if (lab_other.Text != "")
                res = res + other + lab_other.Text;
            if (RoadTypeStr != "")
                res = res + RoadTypeStr;
            lab_txt.Text = res;
            #endregion
        }
    }
    #endregion
    #region--------convDate2(轉換日期格式)-------
    private string convDate2(string dts)
    {
        DateTime dt = new DateTime();
        if (dts == "")
        {
            return "";
        }
        else if (DateTime.TryParse(dts, out dt) == true)
        {

            return (dt.Year - 1911).ToString() + "/" + dt.Month.ToString() + "/" + dt.Day.ToString();

        }
        else
        {
            return "";
        }
    }
    #endregion

    #region ----------------GridView22_RowDataBound()-------------------
    protected void GridView22_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            //編號
            Label Lab_nos = (Label)e.Row.FindControl("Lab_nos");
            //施工日期
            Label lab_dig_st = (Label)e.Row.FindControl("lab_dig_st");
            Label lab_dig_et = (Label)e.Row.FindControl("lab_dig_et");
            Label lab_dig_dt = (Label)e.Row.FindControl("lab_dig_dt");
            lab_dig_st.Text = convDate2(lab_dig_st.Text);
            lab_dig_et.Text = convDate2(lab_dig_et.Text);
            lab_dig_dt.Text = lab_dig_st.Text + " - " + lab_dig_et.Text;
            //發布日期
            Label lab_keytime = (Label)e.Row.FindControl("lab_keytime");
            lab_keytime.Text = convDate2(lab_keytime.Text);
        }
    }
    #endregion

    //匯出excel
    protected void Button3_Click(object sender, EventArgs e)
    {


        this.GridView22.Visible = true;
        GridView22.DataSource = getDataExcel();
        GridView22.DataBind();
        #region-------區域統計---------------
        DataTable dt = new DataTable();
        for (int i = 0; i < 6; i++)
            dt.Columns.Add(i.ToString());

        DataTable dta = getDatatot();
        int tot = 0;
        for (int i = 0; i < 37; i++)
        {
            for (int j = 0; j < dta.Rows.Count; j++)
            {
                if (areas[i] == dta.Rows[j][0].ToString())
                {
                    areaint[i] = int.Parse(dta.Rows[j][1].ToString());
                    tot = tot + int.Parse(dta.Rows[j][1].ToString());
                }
            }
        }
        dt.Rows.Add(areas[0] + "(" + areaint[0].ToString() + ")", areas[1] + "(" + areaint[1].ToString() + ")", areas[2] + "(" + areaint[2].ToString() + ")", areas[3] + "(" + areaint[3].ToString() + ")", areas[4] + "(" + areaint[4].ToString() + ")", areas[5] + "(" + areaint[5].ToString() + ")");
        dt.Rows.Add(areas[6] + "(" + areaint[6].ToString() + ")", areas[7] + "(" + areaint[7].ToString() + ")", areas[8] + "(" + areaint[8].ToString() + ")", areas[9] + "(" + areaint[9].ToString() + ")", areas[10] + "(" + areaint[10].ToString() + ")", areas[11] + "(" + areaint[11].ToString() + ")");
        dt.Rows.Add(areas[12] + "(" + areaint[12].ToString() + ")", areas[13] + "(" + areaint[13].ToString() + ")", areas[14] + "(" + areaint[14].ToString() + ")", areas[15] + "(" + areaint[15].ToString() + ")", areas[16] + "(" + areaint[16].ToString() + ")", areas[17] + "(" + areaint[17].ToString() + ")");
        dt.Rows.Add(areas[18] + "(" + areaint[18].ToString() + ")", areas[19] + "(" + areaint[19].ToString() + ")", areas[20] + "(" + areaint[20].ToString() + ")", areas[21] + "(" + areaint[21].ToString() + ")", areas[22] + "(" + areaint[22].ToString() + ")", areas[23] + "(" + areaint[23].ToString() + ")");
        dt.Rows.Add(areas[25] + "(" + areaint[25].ToString() + ")", areas[26] + "(" + areaint[26].ToString() + ")", areas[27] + "(" + areaint[27].ToString() + ")", areas[28] + "(" + areaint[28].ToString() + ")", areas[29] + "(" + areaint[29].ToString() + ")", areas[30] + "(" + areaint[30].ToString() + ")");
        dt.Rows.Add(areas[31] + "(" + areaint[31].ToString() + ")", areas[32] + "(" + areaint[32].ToString() + ")", areas[33] + "(" + areaint[33].ToString() + ")", areas[34] + "(" + areaint[34].ToString() + ")", areas[35] + "(" + areaint[35].ToString() + ")", areas[36] + "(" + areaint[36].ToString() + ")");
        dt.Rows.Add(areas[24] + "(" + areaint[24].ToString() + ")", "", "", "", "", "");
        Label16.Text = tot.ToString();
        dt.Rows.Add(Label15.Text + Label16.Text + Label17.Text);
        this.GridView3.DataSource = dt;
        this.GridView3.DataBind();
        #endregion

        ExcelUtil eu = new ExcelUtil("", "");
        eu.AddGrid(this.GridView3, "行政區全部案件");
        eu.AddGrid(this.GridView22, "今日案件查詢結果");

        eu.Export(this, Server.UrlEncode("今日案件查詢結果"));
    }

    private DataTable getDataExcel()
    {

        string sqlstr = "";
        string sql1 = "";
        string sql4 = "";
        string sql5 = "";
        string sql6 = "", sql6_1 = "", sql6_2 = "", sql6_3 = "";
        string sdt = DateTime.Now.ToShortDateString() + " 00:00:00";
        string edt = DateTime.Now.ToShortDateString() + " 23:59:59";
        sql1 = sql1 + " and ((dig_st>='" + sdt + "' and dig_et<='" + edt + "') or (dig_st<='" + sdt + "' and  dig_et<'" + edt + "' and dig_et>='" + sdt + "') " +
                         "or (dig_st>='" + sdt + "' and dig_st<'" + edt + "' and dig_et>='" + edt + "') or (dig_st<'" + sdt + "' and dig_et>='" + sdt + "' and dig_et<='" + sdt + "') " +
                         "or (dig_st<'" + sdt + "' and dig_et>'" + edt + "')) ";
        //地址-一般案件
        if (!string.IsNullOrEmpty(SQLInJect(tb_pos.Text)))
        {
            sql6 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or ppcodeName like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_1 = " and (b.WorkSN like '%" + SQLInJect(tb_pos.Text) + "%' or PIPE_CMP_1.PLINE_CMP_ABBR like '%" + SQLInJect(tb_pos.Text) + "%' or b.TargetLBName like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_2 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
            sql6_3 = " and (postion like '%" + SQLInJect(tb_pos.Text) + "%' or pipe_cmp.[PLINE_CMP_ABBR] like '%" + SQLInJect(tb_pos.Text) + "%' or area like '%" + SQLInJect(tb_pos.Text) + "%')";
        }
        //地址-緊急案件
        if (!string.IsNullOrEmpty(tb_pos.Text))
        {
        }


        sqlstr = "select nos,b.TargetLBName AS area," +
                  "licenses,dig_st,dig_et,ppcode,a.userid," +
                  "b.WorkSN AS postion," +
                  "keytime,'一般' [type]," +
                  "PIPE_CMP_1.PLINE_CMP_ABBR AS ppcodeName," +
                  "USERMANAGER_1.Emp_Name AS userName, " +
                 "'' Tar_l,'' Tar_w,'' sidewalk_l,'' sidewalk_w,'' lid,'' other,b.ConstName as labTemp,b.caseid " +
                  ",b.RoadType as RoadType0,convert(varchar,b.[Length]) as Length0,convert(varchar,b.Width) as Width0,convert(varchar,b.Depth) as Depth0,convert(varchar,b.Point) as Point0,convert(varchar,b.Area) as Area0,b.RoadType1,convert(varchar,b.Length1) as Length1,convert(varchar,b.Width1) as Width1,convert(varchar,b.Depth1) as Depth1,convert(varchar,b.Point1) as Point1,convert(varchar,b.Area1) as Area1,b.RoadType2,convert(varchar,b.Length2) as Length2,convert(varchar,b.Width2) as Width2,convert(varchar,b.Depth2) as Depth2,convert(varchar,b.Point2) as Point2,convert(varchar,b.Area2) as Area2,c.lng lon,c.lat lat " +
                 ",(convert(varchar,Supervise)+case when Supervise_Tel<>'' or Supervise_Tel is not null then case when Substring(Rtrim(Ltrim(Supervise_Tel)),1,2)<>'09' then '\n'+convert(varchar,Supervise_Tel) else '' end end ) as mySupervise" +
                 ", (convert(varchar,Factory)+case when Factory_Man_Tel<>'' or Factory_Man_Tel is not null then case when Substring(Rtrim(Ltrim(Factory_Man_Tel)),1,2)<>'09' then '\n'+convert(varchar,Factory_Man_Tel) else '' end end )  as myFactory " +
                  " from (select * from dbo.Pipe_UsuallyCaseSame where CONVERT(date,getdate()) between CONVERT(date,dig_st) and CONVERT(date,dig_et) ) AS a INNER JOIN dbo.View_CaseBasic AS b ON a.caseid = b.CaseID INNER JOIN dbo.PIPE_CMP AS PIPE_CMP_1 ON a.ppcode = PIPE_CMP_1.PLINE_CMP_NO INNER JOIN dbo.USERMANAGER AS USERMANAGER_1 ON a.userid = USERMANAGER_1.Emp_Login INNER JOIN (select ROW_NUMBER() over (Partition by CaseNo order by CaseNo) as Rnum,lat,lng,CaseNo from dbo.AppBasic_Dig where CaseNo in (select caseid from dbo.Pipe_UsuallyCaseSame where CONVERT(date,getdate()) between CONVERT(date,dig_st) and CONVERT(date,dig_et))) c ON a.caseid=c.CaseNo and c.Rnum=1 where 1=1 " +
                   sql1 + sql6_1 +
                  " union all " +
                  " select nos,area,licenses,dig_st,dig_et,ppcode,usermanager.userid,postion,keytime,'緊急' [type]," +
                  "pipe_cmp.[PLINE_CMP_ABBR] ppcodeName," +
                  "usermanager.Emp_name userName, " +
                  "Tar_l,Tar_w,sidewalk_l,sidewalk_w,lid,other,'' labTemp,'' caseid " +
                  ",'' RoadType0,'' Length0,'' Width0,'' Depth0,'' Point0,'' Area0,'' RoadType1,'' Length1,'' Width1,'' Depth1,'' Point1,'' Area1,'' RoadType2,'' Length2,'' Width2,'' Depth2,'' Point2,'' Area2,lon,lat,(convert(varchar,emercont)+case when tel<>'' or tel is not null then case when Substring(Rtrim(Ltrim(tel)),1,2)<>'09' then '\n'+convert(varchar,tel) else '' end end) mySupervise,'' myFactory " +
                  " from Pipe_UsuallyCaseUrgent left join usermanager on Pipe_UsuallyCaseUrgent.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_UsuallyCaseUrgent.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_2 +
                    " union all " +
                    " select nos,area,licenses,dig_st,dig_et,ppcode,usermanager.userid,postion,keytime,'缺失' [type]," +
                    "pipe_cmp.[PLINE_CMP_ABBR] ppcodeName," +
                    "usermanager.Emp_name userName, " +
                    "Tar_l,Tar_w,sidewalk_l,sidewalk_w,lid,other,'' labTemp,'' caseid " +
                    ",'' RoadType0,'' Length0,'' Width0,'' Depth0,'' Point0,'' Area0,'' RoadType1,'' Length1,'' Width1,'' Depth1,'' Point1,'' Area1,'' RoadType2,'' Length2,'' Width2,'' Depth2,'' Point2,'' Area2,lon,lat,(convert(varchar,emercont)+case when tel<>'' or tel is not null then case when Substring(Rtrim(Ltrim(tel)),1,2)<>'09' then '\n'+convert(varchar,tel) else '' end end) mySupervise,'' myFactory " +
                    " from Pipe_SelfInspections left join usermanager on Pipe_SelfInspections.userid = usermanager.Emp_Login  left join pipe_cmp on Pipe_SelfInspections.ppcode=pipe_cmp.PLINE_CMP_NO where 1=1 " + sql1 + sql6_3;

        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY area";
        string sqlFormat = string.Format(
           "SELECT * FROM (SELECT row_number() over (ORDER BY keytime desc) AS RN, " +
           "{1} FROM ({0}) B)C {4} ",
           sqlstr,
           strSQL_T,
           "",
           "",
           strSQL_Order
           );

        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
    }

    #endregion


    #region ----------------BindGrid2(GW)-------------------
    protected void BindGrid2(AspNetPager AspNetPager_, GridView GVList)
    {
        DataSet dt = new DataSet();
        dt = getData2a();
        //AspNetPager_.RecordCount = getDataCount2();
        AspNetPager_.RecordCount = 0;

        GVList.DataSource = dt;
        GVList.DataBind();
        labText.Text = "";
        if (dt.Tables[0].Rows.Count > 0)
        {
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
            //Button3.Visible = true;
            GridView3.Visible = true;
        }
    }
    private DataSet getData2a()
    {
        int endIndex = AspNetPager1.StartRecordIndex + AspNetPager1.PageSize - 1;
        //int endIndex = 0;
        string sqlstr = "";
        string sql1 = "";

        if (!string.IsNullOrEmpty(SQLInJect(TextBox1.Text)))
        {
            sql1 = " and (TD_TOWN like '%" + SQLInJect(TextBox1.Text) + "%' or TD_NAME like '%" + SQLInJect(TextBox1.Text) + "%')";
        }


        sqlstr = "select convert(varchar,TD_CODE ) sysid,convert(varchar,TD_CODE ) case_no,'' from_no,ADM_CODE pmt_no,ADV_DP company,TD_TOWN Area,'' location,'' phone,TD_NAME REASON,'' DATE_DIG_S,'' DATE_DIG_E,'' DATE_EXT_S,'' DATE_EXT_E,GIS_X CenterLng,GIS_Y CenterLat,'' FacilitiesType,'局內' [mytype],'' Supervise,'' Supervise_Tel,'' Factory,'' Factory_Man,'' Factory_Man_Tel,'' Pic_Url_1,'' Pic_Url_2,'Y' myCPC from CPC  where CPC.GIS_X<>'' " + sql1;
        string strSQL_T = "*";
        string strSQL_Order = " ORDER BY sysid";
        string sqlFormat = string.Format(
           "SELECT * FROM (SELECT  " +
           "{1} FROM ({0}) B)C {4} ;",
           sqlstr,
           strSQL_T,
           AspNetPager_Result_5.StartRecordIndex,
           endIndex,
           strSQL_Order
           );
        DataSet dtt = SqlHelper.ExecuteDataset(SqlHelper.ConnectionString, CommandType.Text, sqlFormat);
        System.GC.Collect();

        return dtt;
    }
    private int getDataCount2()
    {
        string strCmd = "";
        int cou = 0;
        string sql1 = "";
        if (!string.IsNullOrEmpty(SQLInJect(TextBox1.Text)))
        {
            sql1 = " and (TD_TOWN like '%" + SQLInJect(TextBox1.Text) + "%' or TD_NAME like '%" + SQLInJect(TextBox1.Text) + "%')";
        }
        strCmd = "select COUNT(*) cou from " +
                 "( " +
                 "select convert(varchar,TD_CODE ) sysid,convert(varchar,TD_CODE ) case_no,'' from_no,ADM_CODE pmt_no,ADV_DP company,TD_TOWN Area,'' location,'' phone,TD_NAME REASON,'' DATE_DIG_S,'' DATE_DIG_E,'' DATE_EXT_S,'' DATE_EXT_E,GIS_X CenterLng,GIS_Y CenterLat,'' FacilitiesType,'局內' [mytype],'' Supervise,'' Supervise_Tel,'' Factory,'' Factory_Man,'' Factory_Man_Tel,'' Pic_Url_1,'' Pic_Url_2,'Y' myCPC from CPC  where CPC.GIS_X<>'' " + sql1+
                ") bb;";
        //Response.Write(strCmd+"<br>");
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader dr = Sqlcmd.ExecuteReader())
                    {
                        if (dr != null)
                        {
                            if (dr.Read())
                            {
                                cou = int.Parse(dr["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        return cou;
    }
    protected void GridView2_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {

            #region-------------施工位置----------------
            Literal Literal_Map2 = (Literal)e.Row.FindControl("Literal_Map2");
            Label Label_X2 = (Label)e.Row.FindControl("lab_X2");
            Label Label_Y2 = (Label)e.Row.FindControl("lab_Y2");
            string lat = DataBinder.Eval(e.Row.DataItem, "CenterLat").ToString();
            string lon = DataBinder.Eval(e.Row.DataItem, "CenterLng").ToString();
            if (lat != "")
            {
                Literal_Map2.Text = "<a href=javascript:golatLng(" + lat + "," + lon + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";
            }
            Literal_Map2.Visible = true;
            Label_X2.Visible = false;
            Label_Y2.Visible = false;
            #endregion
        }
    }
    protected void Button1_Click(object sender, EventArgs e)
    {
        BindGrid2(AspNetPager1, GridView2);
    }
    #endregion

    #region ----------------VerifyRenderingInServerForm()-------------------
    public override void VerifyRenderingInServerForm(Control control)
    {
        // '處理'GridView' 的控制項 'GridView' 必須置於有 runat=server 的表單標記之中   
    }
    #endregion

    #region ----------------路平專案(GW)-------------------
    protected void BindGridLuPing(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        //AspNetPager_.RecordCount = getDataCountLuPing();
        AspNetPager_.RecordCount = 0;
        dt = getDataLuPing();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labTextLuPing.Text = "";
        if (dt.Rows.Count > 0)
        {
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            labTextLuPing.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
    }
    protected void AspNetPager_Result_PageChanged_LuPing(object sender, EventArgs e)
    {
        this.GVList_Result_LuPing.Visible = true;
        BindGridLuPing(this.AspNetPager_Result_LuPing, this.GVList_Result_LuPing);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountLuPing()
    {
        int cou = 0;
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;

        string sql_case = "", sql_case2 = "";
        if (!SQLInJect(tb_LuPing.Text).Trim().Equals(""))
        {
            sql_case = " and (WARD+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or WARD2+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or WARD3+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_LuPing.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_LuPing.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_LuPing.Text) + "%' or rpoly like '%" + SQLInJect(tb_LuPing.Text) + "%' or pj_name like '%" + SQLInJect(tb_LuPing.Text) + "%') ";
        }

        string strCmd = "select sum(a.cou) cou from (";
        strCmd += "select COUNT(*) cou from RoadFee where 1=1 and (States<>'9' or States is null) and RoadType='1' and ((FINISH_DATE >= '" + Find_E1a + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from RoadFee where 1=1 and (States<>'9' or States is null) and RoadType='1' and (((completion_time='' or completion_time is null) and (FINISH_DATE='' or FINISH_DATE is null)) or ((completion_time='' or completion_time is null) and (FINISH_DATE is not null))) and RoadType='1'  " + sql_case + " ";//預定
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from Digroad where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from Digroad where 1=1 and (States<>'9' or States is null) and (keep_btime is not null and keep_btime<>'' and etime='' and completion_time='')  " + sql_case2 + "";//預定
        strCmd += ") a;";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        return cou;
    }

    private DataTable getDataLuPing()
    {
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;
        string sql_case = "", sql_case2 = "", sql_case3 = "";
        if (!SQLInJect(tb_LuPing.Text).Trim().Trim().Equals(""))
        {
            sql_case = " and (WARD+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or WARD2+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or WARD3+'區' like '%" + SQLInJect(tb_LuPing.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_LuPing.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_LuPing.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_LuPing.Text) + "%' or rpoly like '%" + SQLInJect(tb_LuPing.Text) + "%' or pj_name like '%" + SQLInJect(tb_LuPing.Text) + "%') ";
        }
        int endIndex = AspNetPager_Result_LuPing.StartRecordIndex + AspNetPager_Result_LuPing.PageSize - 1;
        

				string sqlstr = "select RF.*,CONVERT(varchar,RFD.lat)+','+CONVERT(varchar,RFD.lng) as latlng from (select '' fk_emp_id,caseid,'1' mytype,CONVERT(varchar,id) id,WARD+'區' WARD,ROAD_NAME,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,OFFICE,CONVERT(varchar,ROAD_SECTION) ROAD_SECTION,case when FINISH_DATE is not null then (CONVERT(varchar, CONVERT(int, substring(CONVERT(varchar, FINISH_DATE, 101), 7, 4)) - 1911)) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 1, 2) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 4, 2) else '' end FINISH_DATE,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from RoadFee where 1=1 and (States<>'9' or States is null) and RoadType='1' and ((FINISH_DATE >= '" + Find_E1a + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case + ") RF left join ROADFEE_DIG RFD on RF.caseid=RFD.caseid1 ";
        sqlstr += "UNION ";
				sqlstr += "select RF.*,CONVERT(varchar,RFD.lat)+','+CONVERT(varchar,RFD.lng) as latlng from (select '' fk_emp_id,caseid,'1' mytype,CONVERT(varchar,id) id,WARD+'區' WARD,ROAD_NAME,case when keep_btime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_btime, 1, 3)))) + '/' + substring(keep_btime, 4, 2) + '/' + substring(keep_btime, 6, 2) else '' end keep_btime,case when keep_etime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_etime, 1, 3)))) + '/' + substring(keep_etime, 4, 2) + '/' + substring(keep_etime, 6, 2) else '' end keep_etime,OFFICE,CONVERT(varchar,ROAD_SECTION) ROAD_SECTION,case when FINISH_DATE is not null then (CONVERT(varchar, CONVERT(int, substring(CONVERT(varchar, FINISH_DATE, 101), 7, 4)) - 1911)) + '' + substring(CONVERT(varchar, FINISH_DATE, 101), 1, 2) + '' + substring(CONVERT(varchar, FINISH_DATE, 101), 4, 2) else '' end FINISH_DATE,completion_time from RoadFee where 1=1 and (States<>'9' or States is null) and RoadType='1' and (((completion_time='' or completion_time is null) and (FINISH_DATE='' or FINISH_DATE is null)) or ((completion_time='' or completion_time is null) and (FINISH_DATE is not null))) and RoadType='1'  " + sql_case + ")RF left join ROADFEE_DIG RFD on RF.caseid=RFD.caseid1 ";
        sqlstr += "UNION ";        
				sqlstr += "select DR.*,DC.latlng from (select fk_emp_id,'' caseid,'2' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,case when etime is not null then (CONVERT(varchar, CONVERT(int, substring(etime, 1, 3)))) + '/' + substring(etime, 4, 2) + '/' + substring(etime, 6, 2) else '' end etime,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from Digroad where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + ")DR left join (select ROW_NUMBER() over (Partition by caseid order by caseid) as Rnum,CONVERT(varchar,lat)+','+CONVERT(varchar,lng) as latlng,caseid1 as Caseid from DIGCASE where caseid1 in (select id from DIGROAD where (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + " )) DC on DR.caseid=DC.caseid and DC.Rnum=1 ";
        sqlstr += "UNION ";
        sqlstr += "select DR.*,DC.latlng from (select fk_emp_id,'' caseid,'2' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_btime, 1, 3)))) + '/' + substring(keep_btime, 4, 2) + '/' + substring(keep_btime, 6, 2) else '' end keep_btime,case when keep_etime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_etime, 1, 3)))) + '/' + substring(keep_etime, 4, 2) + '/' + substring(keep_etime, 6, 2) else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,etime,completion_time from Digroad where 1=1 and (States<>'9' or States is null) and (keep_btime is not null and keep_btime<>'' and etime='' and completion_time='')  " + sql_case2 + ") DR left join (select ROW_NUMBER() over (Partition by caseid order by caseid) as Rnum,CONVERT(varchar,lat)+','+CONVERT(varchar,lng) as latlng,caseid1 as Caseid from DIGCASE where caseid1 in (select id from DIGROAD where (States<>'9' or States is null) and (keep_btime is not null and keep_btime<>'' and etime='' and completion_time='')" + sql_case2 + " )) DC on DR.caseid=DC.Caseid and DC.Rnum=1";
        string strSQL_T = "*";
        string strSQL_Order = " order by completion_time desc,FINISH_DATE desc,id Desc";
        string sqlFormat = string.Format(
           "SELECT * FROM (SELECT  " +
           "{1} FROM ({0}) B)C {4} ;",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_LuPing.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        myClass myclass = new myClass();
        myclass.sqlWrtieLineRunTimeLog(sqlFormat);
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }
    }
    protected void GVList_Result_LuPing_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {

            e.Row.Cells[0].Text = !DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim().Equals("") ? DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim() : DataBinder.Eval(e.Row.DataItem, "id").ToString().Trim();
            if ((DataBinder.Eval(e.Row.DataItem, "WARD").ToString().Trim().Equals("請選擇區")))
            {
                e.Row.Cells[1].Text = "";
            }
            if (DataBinder.Eval(e.Row.DataItem, "completion_time").ToString().Trim() != "")
            {
                e.Row.Cells[5].Text = DataBinder.Eval(e.Row.DataItem, "FINISH_DATE").ToString().Trim() + "至" + DataBinder.Eval(e.Row.DataItem, "completion_time").ToString().Trim();
            }
            else
            {
                e.Row.Cells[5].Text = "";
            }
            
            Literal Literal_Map = (Literal)e.Row.FindControl("Literal_Map");
            string latlon = DataBinder.Eval(e.Row.DataItem, "latlng").ToString();            
            if (latlon != "")
            {
                Literal_Map.Text = "<a href=javascript:golatLng2(" + latlon + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";
            }
            Literal_Map.Visible = true;
        }
    }
    protected void btnLuPing_Click(object sender, EventArgs e)
    {
        BindGridLuPing(this.AspNetPager_Result_LuPing, this.GVList_Result_LuPing);
    }
    #endregion

    #region ----------------預定施工管制(GW)-------------------
    protected void BindGridPreCC(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        //AspNetPager_.RecordCount = getDataCountPreCC();
        AspNetPager_.RecordCount = 0;
        dt = getDataPreCC();
        GVList.DataSource = dt;
        GVList.DataBind();
        labTextPreCC.Text = "";
        if (dt.Rows.Count > 0)
        {
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            labTextPreCC.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
    }
    protected void AspNetPager_Result_PageChanged_PreCC(object sender, EventArgs e)
    {
        this.GVList_Result_PreCC.Visible = true;
        BindGridPreCC(this.AspNetPager_Result_PreCC, this.GVList_Result_PreCC);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountPreCC()
    {
        int cou = 0;
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;

        string sql_case = "", sql_case2 = "", sql_case3="";
        if (!SQLInJect(tb_PreCC.Text).Trim().Trim().Equals(""))
        {
            sql_case = " and (WARD like '%" + SQLInJect(tb_PreCC.Text) + "%' or WARD2 like '%" + SQLInJect(tb_PreCC.Text) + "%' or WARD3 like '%" + SQLInJect(tb_PreCC.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_PreCC.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_PreCC.Text) + "%' or rpoly like '%" + SQLInJect(tb_PreCC.Text) + "%' or pj_name like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
            sql_case3 = " and (area like '%" + SQLInJect(tb_PreCC.Text) + "%' or rpoly like '%" + SQLInJect(tb_PreCC.Text) + "%' or pj_name like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
        }

        string strCmd = "select sum(a.cou) cou from (";
        strCmd += "select COUNT(*) cou from RoadFee where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from Digroad where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case2 + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from DIGPLAN LEFT OUTER JOIN PPBasic ON DIGPLAN.unit_code = PPBasic.PPCode where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case3 + " ";
        strCmd += ") a;";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        return cou;
    }

    private DataTable getDataPreCC()
    {
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;
        string sql_case = "", sql_case2 = "",sql_case3="";
        if (!SQLInJect(tb_PreCC.Text).Trim().Trim().Equals(""))
        {
            sql_case = " and (WARD like '%" + SQLInJect(tb_PreCC.Text) + "%' or WARD2 like '%" + SQLInJect(tb_PreCC.Text) + "%' or WARD3 like '%" + SQLInJect(tb_PreCC.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_PreCC.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_PreCC.Text) + "%' or rpoly like '%" + SQLInJect(tb_PreCC.Text) + "%' or pj_name like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
            sql_case3 = " and (area like '%" + SQLInJect(tb_PreCC.Text) + "%' or rpoly like '%" + SQLInJect(tb_PreCC.Text) + "%' or pj_name like '%" + SQLInJect(tb_PreCC.Text) + "%') ";
        }
        int endIndex = AspNetPager_Result_PreCC.StartRecordIndex + AspNetPager_Result_PreCC.PageSize - 1;
        string sqlstr = "";        
        sqlstr += "select RF.*,CONVERT(varchar,RFD.lat)+','+CONVERT(varchar,RFD.lng) as latlng  from (select '' fk_emp_id,caseid,'1' mytype,CONVERT(varchar,id) id,WARD+'區' WARD,ROAD_NAME,case when keep_btime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_btime, 1, 3)))) + '/' + substring(keep_btime, 4, 2) + '/' + substring(keep_btime, 6, 2) else '' end keep_btime,case when keep_etime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_etime, 1, 3)))) + '/' + substring(keep_etime, 4, 2) + '/' + substring(keep_etime, 6, 2) else '' end keep_etime,OFFICE,CONVERT(varchar,ROAD_SECTION) ROAD_SECTION,case when FINISH_DATE is not null then (CONVERT(varchar, CONVERT(int, substring(CONVERT(varchar, FINISH_DATE, 101), 7, 4)) - 1911)) + '' + substring(CONVERT(varchar, FINISH_DATE, 101), 1, 2) + '' + substring(CONVERT(varchar, FINISH_DATE, 101), 4, 2) else '' end FINISH_DATE,completion_time from RoadFee	where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case + " ) RF left join RoadFee_Dig RFD on RF.caseid=RFD.caseid1 ";        
        sqlstr += "UNION ";
				sqlstr += "select DR.*,DC.latlng from (select fk_emp_id,'' caseid,'2' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_btime, 1, 3)))) + '/' + substring(keep_btime, 4, 2) + '/' + substring(keep_btime, 6, 2) else '' end keep_btime,case when keep_etime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_etime, 1, 3)))) + '/' + substring(keep_etime, 4, 2) + '/' + substring(keep_etime, 6, 2) else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,etime,completion_time from Digroad where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case2 + ") DR left join (select ROW_NUMBER() over (Partition by caseid1 order by caseid1) as Rnum,CONVERT(varchar,lat) + ',' + CONVERT(varchar,lng) as latlng,caseid1 as caseid from DIGCASE where caseid1 in (select caseid from Digroad where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case2 + " )) DC on DR.Caseid=Dc.caseid and DC.Rnum=1 ";
				sqlstr += "UNION ";
        sqlstr += "select DP.*,DPD.latlng from (select fk_emp_id,'' caseid,'3' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_btime, 1, 3)))) + '/' + substring(keep_btime, 4, 2) + '/' + substring(keep_btime, 6, 2) else '' end keep_btime,case when keep_etime is not null then (CONVERT(varchar, CONVERT(int, substring(keep_etime, 1, 3)))) + '/' + substring(keep_etime, 4, 2) + '/' + substring(keep_etime, 6, 2) else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,etime,completion_time from DIGPLAN LEFT OUTER JOIN PPBasic ON DIGPLAN.unit_code = PPBasic.PPCode where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case3 + ") DP left join (select ROW_NUMBER() over (Partition by caseid1 order by caseid1) as Rnum,CONVERT(varchar,lat) + ',' + CONVERT(varchar,lng) as latlng,caseid1 as caseid from DIGPLAN_DIG where caseid1 in ( select id from DIGPLAN where 1=1 and (States<>'9' or States is null) and (keep_etime >= '" + Find_E1 + "') and (keep_btime is not null and keep_btime<>'') " + sql_case3 + ")) DPD on DP.id=DPD.caseid and DPD.Rnum=1";
        
        
        string strSQL_T = "*";
        string strSQL_Order = " order by completion_time desc,FINISH_DATE desc,id Desc";
        string sqlFormat = string.Format(
           "SELECT * FROM (SELECT  " +
           "{1} FROM ({0}) B)C {4} ;",
       sqlstr,
       strSQL_T,
       AspNetPager_Result_PreCC.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }
            return dtt;

        }

    }
    protected void GVList_Result_PreCC_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
						Literal Literal_Map = (Literal)e.Row.FindControl("Literal_Map");
						string latlng = DataBinder.Eval(e.Row.DataItem, "latlng").ToString();
						string caseid = DataBinder.Eval(e.Row.DataItem, "Caseid").ToString() != "0" ? DataBinder.Eval(e.Row.DataItem, "Caseid").ToString() : "";
						if (latlng != "")
						{
							Literal_Map.Text = "<a href=javascript:golatLng2(" + latlng + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";							
						}
						Literal_Map.Visible = true;
            e.Row.Cells[0].Text = !DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim().Equals("") ? DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim() : DataBinder.Eval(e.Row.DataItem, "id").ToString().Trim();
            e.Row.Cells[5].Text = DataBinder.Eval(e.Row.DataItem, "keep_btime").ToString().Trim() + "至" + DataBinder.Eval(e.Row.DataItem, "keep_etime").ToString().Trim();
        }
    }
    protected void btnPreCC_Click(object sender, EventArgs e)
    {
        BindGridPreCC(this.AspNetPager_Result_PreCC, this.GVList_Result_PreCC);
    }
    #endregion

    #region ----------------完工禁挖管制(GW)-------------------
    protected void BindGridCBC(AspNetPager AspNetPager_, GridView GVList)
    {
        DataTable dt = new DataTable();
        //AspNetPager_.RecordCount = getDataCountCBC();
        AspNetPager_.RecordCount = 0;
        dt = getDataCBC();
        //Response.Write(AspNetPager_.RecordCount.ToString());
        GVList.DataSource = dt;
        GVList.DataBind();
        labTextCBC.Text = "";
        if (dt.Rows.Count > 0)
        {
            AspNetPager_.CustomInfoHTML = "目前在：頁次 第<span style='color: #ff0066'> " + AspNetPager_.CurrentPageIndex + "</span> / " + AspNetPager_.PageCount;
            AspNetPager_.CustomInfoHTML += " 頁（共<span style='color: #ff0066'> " + AspNetPager_.RecordCount +
                                           "</span> 筆｜共<span style='color: #ff0066'> " + AspNetPager_.PageCount + "</span>&nbsp;頁）";

            AspNetPager_.CustomInfoHTML += "&nbsp;<br>案件：" + AspNetPager_.StartRecordIndex + "-" + AspNetPager_.EndRecordIndex;
            GVList.Visible = true;
        }
        else
        {
            labTextCBC.Text = "<br><br><br><br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;無案件<br>";
        }
    }
    protected void AspNetPager_Result_PageChanged_CBC(object sender, EventArgs e)
    {
        this.GVList_Result_CBC.Visible = true;
        BindGridCBC(this.AspNetPager_Result_CBC, this.GVList_Result_CBC);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }

    private int getDataCountCBC()
    {
        int cou = 0;
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;

        string sql_case = "", sql_case2 = "", sql_case3 = "";
        if (!SQLInJect(tb_CBC.Text).Trim().Equals(""))
        {
            sql_case = " and (WARD like '%" + SQLInJect(tb_CBC.Text) + "%' or WARD2 like '%" + SQLInJect(tb_CBC.Text) + "%' or WARD3 like '%" + SQLInJect(tb_CBC.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_CBC.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_CBC.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_CBC.Text) + "%' or rpoly like '%" + SQLInJect(tb_CBC.Text) + "%' or pj_name like '%" + SQLInJect(tb_CBC.Text) + "%') ";
            sql_case3 = " and (area like '%" + SQLInJect(tb_CBC.Text) + "%' or rpoly like '%" + SQLInJect(tb_CBC.Text) + "%' or pj_name like '%" + SQLInJect(tb_CBC.Text) + "%') ";
        }

        string strCmd = "select sum(a.cou) cou from (";
        strCmd += "select COUNT(*) cou from RoadFee where 1=1 and (States<>'9' or States is null) and ((FINISH_DATE >= '" + Find_E1a + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from Digroad where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + " ";
        strCmd += "UNION ";
        strCmd += "select COUNT(*) cou from DIGPLAN LEFT OUTER JOIN PPBasic ON DIGPLAN.unit_code = PPBasic.PPCode where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case3 + " ";
        strCmd += ") a;";
        //Response.Write(strCmd);
        //Response.End();
        try
        {
            using (SqlConnection myConnection = new SqlConnection(SqlHelper.ConnectionString))
            {
                ConnectionState previousConnectionState = myConnection.State;
                using (SqlCommand Sqlcmd = new SqlCommand(strCmd, myConnection))
                {
                    Sqlcmd.CommandTimeout = 60;
                    if (myConnection.State == ConnectionState.Closed)
                    {
                        myConnection.Open();
                    }
                    using (SqlDataReader reader = Sqlcmd.ExecuteReader())
                    {
                        if (reader != null)
                        {
                            if (reader.Read())
                            {
                                cou = int.Parse(reader["cou"].ToString());
                            }
                        }
                        else
                        {
                            cou = 0;
                        }
                    }
                }
            }
        }
        catch (Exception)
        {
        }
        return cou;
    }

    private DataTable getDataCBC()
    {
        string yy = (DateTime.Now.Year - 1911).ToString();
        string mm = (DateTime.Now.Month).ToString().Length < 2 ? "0" + (DateTime.Now.Month).ToString() : (DateTime.Now.Month).ToString();
        string dd = (DateTime.Now.Day).ToString().Length < 2 ? "0" + (DateTime.Now.Day).ToString() : (DateTime.Now.Day).ToString();
        string Find_E1a = DateTime.Now.Year.ToString() + "/" + mm + "/" + dd;
        string Find_E1 = yy + mm + dd;
        string sql_case = "", sql_case2 = "", sql_case3 = "";
        if (!SQLInJect(tb_CBC.Text).Trim().Trim().Equals(""))
        {
            sql_case = " and (WARD like '%" + SQLInJect(tb_CBC.Text) + "%' or WARD2 like '%" + SQLInJect(tb_CBC.Text) + "%' or WARD3 like '%" + SQLInJect(tb_CBC.Text) + "%' or ROAD_SECTION like '%" + SQLInJect(tb_CBC.Text) + "%' or ROAD_NAME like '%" + SQLInJect(tb_CBC.Text) + "%') ";
            sql_case2 = " and (area like '%" + SQLInJect(tb_CBC.Text) + "%' or rpoly like '%" + SQLInJect(tb_CBC.Text) + "%' or pj_name like '%" + SQLInJect(tb_CBC.Text) + "%') ";
            sql_case3 = " and (area like '%" + SQLInJect(tb_CBC.Text) + "%' or rpoly like '%" + SQLInJect(tb_CBC.Text) + "%' or pj_name like '%" + SQLInJect(tb_CBC.Text) + "%') ";
        }
				//
        int endIndex = AspNetPager_Result_CBC.StartRecordIndex + AspNetPager_Result_CBC.PageSize - 1;
        string sqlstr = "";
        //sqlstr += "select '' fk_emp_id,caseid,'1' mytype,CONVERT(varchar,id) id,WARD+'區' WARD,ROAD_NAME,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,OFFICE,CONVERT(varchar,ROAD_SECTION) ROAD_SECTION,case when FINISH_DATE is not null then (CONVERT(varchar, CONVERT(int, substring(CONVERT(varchar, FINISH_DATE, 101), 7, 4)) - 1911)) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 1, 2) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 4, 2) else '' end FINISH_DATE,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from RoadFee where 1=1 and (States<>'9' or States is null) and ((FINISH_DATE >= '" + Find_E1a + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case + " ";
        sqlstr += "select RF.*,convert(varchar,RFD.lat) +','+convert(varchar,RFD.lng) as latlng from(select '' fk_emp_id,caseid,'1' mytype,CONVERT(varchar,id) id,WARD+'區' WARD,ROAD_NAME,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,OFFICE,CONVERT(varchar,ROAD_SECTION) ROAD_SECTION,case when FINISH_DATE is not null then (CONVERT(varchar, CONVERT(int, substring(CONVERT(varchar, FINISH_DATE, 101), 7, 4)) - 1911)) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 1, 2) + '/' + substring(CONVERT(varchar, FINISH_DATE, 101), 4, 2) else '' end FINISH_DATE,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from RoadFee where 1=1 and (States<>'9' or States is null) and ((FINISH_DATE >= '" + Find_E1a + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case + ") RF left join ROADFEE_DIG RFD on RF.caseid=RFD.caseid1 ";
        sqlstr += "UNION ";
        //sqlstr += "select fk_emp_id,'' caseid,'2' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,case when etime is not null then (CONVERT(varchar, CONVERT(int, substring(etime, 1, 3)))) + '/' + substring(etime, 4, 2) + '/' + substring(etime, 6, 2) else '' end etime,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from Digroad where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + " ";
        sqlstr += "select DR.*,DC.latlng from (select fk_emp_id,'' caseid,'2' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,case when etime is not null then (CONVERT(varchar, CONVERT(int, substring(etime, 1, 3)))) + '/' + substring(etime, 4, 2) + '/' + substring(etime, 6, 2) else '' end etime,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from Digroad where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case2 + ")DR left join (select ROW_NUMBER() over (Partition by caseid order by caseid) as Rnum,CONVERT(varchar,lat)+','+CONVERT(varchar,lng) as latlng,caseid1 as Caseid from DIGCASE where caseid1 in (select id from DIGROAD where (States<>'9' or States is null) and ((etime >= '1071005') or (completion_time >= '1071005')))) DC on	DR.Caseid=DC.caseid and DC.Rnum=1 ";
        sqlstr += "UNION ";        
        //sqlstr += "select fk_emp_id,'' caseid,'3' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,case when etime is not null then (CONVERT(varchar, CONVERT(int, substring(etime, 1, 3)))) + '/' + substring(etime, 4, 2) + '/' + substring(etime, 6, 2) else '' end etime,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from DIGPLAN LEFT OUTER JOIN PPBasic ON DIGPLAN.unit_code = PPBasic.PPCode where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case3 + " ";
        sqlstr += "select DP.*,DPD.latlng from(select fk_emp_id,'' caseid,'3' mytype,CONVERT(varchar,id) id,area,pj_name,case when keep_btime is not null then keep_btime else '' end keep_btime,case when keep_etime is not null then keep_etime else '' end keep_etime,plineno,CONVERT(varchar,rpoly) rpoly,case when etime is not null then (CONVERT(varchar, CONVERT(int, substring(etime, 1, 3)))) + '/' + substring(etime, 4, 2) + '/' + substring(etime, 6, 2) else '' end etime,case when completion_time is not null then (CONVERT(varchar, CONVERT(int, substring(completion_time, 1, 3)))) + '/' + substring(completion_time, 4, 2) + '/' + substring(completion_time, 6, 2) else '' end completion_time from DIGPLAN LEFT OUTER JOIN PPBasic ON DIGPLAN.unit_code = PPBasic.PPCode where 1=1 and (States<>'9' or States is null) and ((etime >= '" + Find_E1 + "') or (completion_time >= '" + Find_E1 + "')) " + sql_case3 + ") DP Left join(select ROW_NUMBER() over (Partition by caseid1 order by caseid1) as Rnum,CONVERT(varchar,lat) + ',' + CONVERT(varchar,lng) as latlng,caseid1 as caseid from DIGPLAN_DIG where caseid1 in ( select id from DIGPLAN where 1=1 and (States<>'9' or States is null) and ((etime >= '1071005') or (completion_time >= '1071005')))) DPD on DP.id=DPD.caseid and DPD.Rnum=1";
        string strSQL_T = "*";
        string strSQL_Order = " order by completion_time desc,FINISH_DATE desc,id Desc";
        string sqlFormat = string.Format(
            "SELECT * FROM (SELECT  " +
           "{1} FROM ({0}) B)C {4} ;",
      sqlstr,
       strSQL_T,
       AspNetPager_Result_CBC.StartRecordIndex,
       endIndex,
       strSQL_Order
       );
        //Response.Write(sqlFormat);
        //Response.End();
        if (conn.State == ConnectionState.Closed)
        {
            conn.Open();
        }
        DataTable dtt = new DataTable();
        using (SqlDataAdapter daa = new SqlDataAdapter(sqlstr, conn))
        {
            try
            {
                daa.Fill(dtt);

                daa.Dispose();
            }
            catch (Exception)
            {

                throw;
            }
            finally
            {
                conn.Close();
                System.GC.Collect();
            }

            // 參考 https://forums.asp.net/t/1997966.aspx?Sort+Gridview+bound+to+datatable
            DataView dv1 = new DataView(dtt);
            dv1.Sort = "completion_time desc, FINISH_DATE desc"; //加入排序日期(倒序)
            dtt = dv1.ToTable();
            return dtt;

        }
    }
    protected void GVList_Result_CBC_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
						Literal Literal_Map = (Literal)e.Row.FindControl("Literal_Map");
						string latlon = DataBinder.Eval(e.Row.DataItem, "latlng").ToString();
						if (latlon != "")
						{
							Literal_Map.Text = "<a href=javascript:golatLng2(" + latlon + "); /><img src='html/image/earth.gif' width='14' border='0' title='施工位置' /></a>";
						}
						Literal_Map.Visible = true;
            e.Row.Cells[0].Text = !DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim().Equals("") ? DataBinder.Eval(e.Row.DataItem, "caseid").ToString().Trim() : DataBinder.Eval(e.Row.DataItem, "id").ToString().Trim();
            e.Row.Cells[5].Text = DataBinder.Eval(e.Row.DataItem, "FINISH_DATE").ToString().Trim() + "至" + DataBinder.Eval(e.Row.DataItem, "completion_time").ToString().Trim();
        }
    }
    protected void btnCBC_Click(object sender, EventArgs e)
    {
        BindGridCBC(this.AspNetPager_Result_CBC, this.GVList_Result_CBC);
    }
    #endregion

    #region ----------------BindDataList(最新消息列表)-------------------
    protected void BindDataList()
    {
        System.DateTime dt2 = System.DateTime.Now;
        TaiwanCalendar tc = new TaiwanCalendar();
        string lastMonth2 = String.Format("{0:D3}", tc.GetYear(dt2)) + String.Format("{0:D2}", tc.GetMonth(dt2)) + String.Format("{0:D2}", tc.GetDayOfMonth(dt2));

        string strSQL = "SELECT NewsID, Topic, (convert(varchar,convert(int,substring(convert(varchar,PubDate,101),7,4))-1911))+'/'+substring(convert(varchar,PubDate,101),1,2)+'/'+substring(convert(varchar,PubDate,101),4,2) as PubDate FROM Announce WHERE  ((Type = 2) AND (DATEDIFF(day, StopDate, GETDATE()) > 900)) ORDER BY PubDate ";
        TNrunsql a = new TNrunsql();

        DataTable dt = a.selectAll(strSQL);
        string message = "<marquee scrollamount='2' DIRECTION='up' onMouseOver='this.stop()' onMouseOut='this.start()' HEIGHT='150'>";

        for (int j = 0; j < dt.Rows.Count; j++)
        {
            message += "<img  src='images/new1.gif' style='border-width:0px;' /><b>" + dt.DefaultView[j]["Topic"].ToString() + "</b>&nbsp;&nbsp;&nbsp;&nbsp;[" + dt.DefaultView[j]["PubDate"].ToString() + "]<br />";
        }
        message += "</marquee>";

        dlHot2.DataSource = a.selectAll(strSQL);
        dlHot2.DataBind();
    }
    #endregion

    #region ----------------BindDataList(市政公告)-------------------
    protected void BindDataList2()
    {
        System.DateTime dt2 = System.DateTime.Now;
        TaiwanCalendar tc = new TaiwanCalendar();
        string lastMonth2 = String.Format("{0:D3}", tc.GetYear(dt2)) + String.Format("{0:D2}", tc.GetMonth(dt2)) + String.Format("{0:D2}", tc.GetDayOfMonth(dt2));

        string strSQL = "SELECT  NewsID, Topic, (convert(varchar,convert(int,substring(convert(varchar,PubDate,101),7,4))-1911))+'/'+substring(convert(varchar,PubDate,101),1,2)+'/'+substring(convert(varchar,PubDate,101),4,2) as PubDate2 FROM Announce WHERE  ((Type = 1) AND (DATEDIFF(day, StopDate, GETDATE()) > 1)) ORDER BY PubDate desc";
        TNrunsql a = new TNrunsql();

        GridView1.DataSource = a.selectAll(strSQL);
        GridView1.DataBind();
    }
    #endregion

    #region ----------------AspNetPager_Result_PageChanged(換頁)-------------------
    protected void AspNetPager_Result_PageChanged(object src, EventArgs e)
    {
        string GrirdViewId = "GVList_Result_" + tc2.ActiveTabIndex;
        string aspnetpageId = "AspNetPager_Result_" + tc2.ActiveTabIndex;
        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        BindGrid_Result(Dist[tc2.ActiveTabIndex], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", aspNetPager, gvlist, tb_0.Text);
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }

    #region ----------------AspNetPager_PageChanged(換頁)-------------------
    protected void AspNetPager_PageChanged_5(object sender, EventArgs e)
    {
        this.GridView0.Visible = true;
        BindGrid(this.AspNetPager_Result_5, this.GridView0);

        // 刻意暫停 2 秒
        Thread.Sleep(1000);//如果沒加,修改後畫面會跑不出來.
    }
    #endregion
    protected void AspNetPager_Result_PageChanged_1(object src, EventArgs e)
    {
        string GrirdViewId = "GVList_Result_" + tc2.ActiveTabIndex;
        string aspnetpageId = "AspNetPager_Result_" + tc2.ActiveTabIndex;

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        string aa = "lb" + tc2.ActiveTabIndex + "_" + hf.Value;
        LinkButton lb = (LinkButton)(tc2.ActiveTab.FindControl(aa));

        BindGrid_Result(lb.Text, lb.Text, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    #endregion

    #region ----------------TabButton_Result_Click(選單)-------------------
    protected void TabButton_Result_Click(object sender, EventArgs e)
    {
        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        string strTabPanel = "TabPanel_Result_aL" + tc2.ActiveTabIndex;
        TabPanel tabPanel = (TabPanel)(tc2.ActiveTab.FindControl(strTabPanel));

        string strUpdatePanel = "UpdatePanel_Result_" + tc2.ActiveTabIndex;
        UpdatePanel updatePanel = (UpdatePanel)(tc2.ActiveTab.FindControl(strUpdatePanel));
        ITemplate iTemplate = updatePanel.ContentTemplate;

        int lb = int.Parse(((LinkButton)sender).ID.ToString().Split(new char[] { '_' })[1]);

        string containerId = "TabContent_Result_" + tc2.ActiveTabIndex;
        Panel panel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        hf.Value = lb.ToString();
        // 顯示某個索引標籤內的 Panel 控制項。
        if (panel != null) panel.Visible = true;

        string GrirdViewId = "GVList_Result_" + tc2.ActiveTabIndex;
        string aspnetpageId = "AspNetPager_Result_" + tc2.ActiveTabIndex;

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;
        if ((tc2.ActiveTabIndex == 0))
        {

            aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(Dist[tc2.ActiveTabIndex], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", "");
            ApplyListInfo.Dispose_Result();

            BindGrid_Result(Dist[tc2.ActiveTabIndex], "'東區', '南區', '北區', '安平區', '安南區', '中西區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區','安定區'", aspNetPager, gvlist, "");
            // 刻意暫停 2 秒
            Thread.Sleep(1000);
        }
        else
        {

            aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(((LinkButton)sender).Text, ((LinkButton)sender).Text, "");
            ApplyListInfo.Dispose_Result();
            BindGrid_Result(((LinkButton)sender).Text, ((LinkButton)sender).Text, aspNetPager, gvlist, "");

            // 刻意暫停 2 秒
            Thread.Sleep(1000);
        }

    }
    #endregion

    protected void TabButton_Result_Click_1_0(object sender, EventArgs e)
    {

        int lb = int.Parse(((LinkButton)sender).ID.ToString().Split(new char[] { '_' })[1]);

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        hf.Value = lb.ToString();
        string containerId = "TabContent_Result_1";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_1";
        string aspnetpageId = "AspNetPager_Result_1";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }
    //臺南市六區
    protected void TabButton_Result_Click_1(object sender, EventArgs e)
    {
        LinkButton lb = (LinkButton)sender;

        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        hid1.Value = lb.Text;
        string containerId = "TabContent_Result_" + index.ToString();
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(lb.Text, lb.Text, "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result(lb.Text, lb.Text, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }
    protected void AspNetPager_Result_PageChanged_11(object src, EventArgs e)
    {
        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));


        BindGrid_Result(hid1.Value, hid1.Value, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    //溪南地區全部案件
    protected void TabButton_Result_Click_2(object sender, EventArgs e)
    {
        LinkButton lb = (LinkButton)sender;

        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        //Page.Header.Title = "TabContent_Result_1";
        hid2.Value = lb.Text;
        string containerId = "TabContent_Result_" + index.ToString();
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(lb.Text, lb.Text, "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result(lb.Text, lb.Text, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    protected void AspNetPager_Result_PageChanged_21(object src, EventArgs e)
    {
        //LinkButton lb = (LinkButton)src;
        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));
        BindGrid_Result(hid2.Value, hid2.Value, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    //北區
    protected void TabButton_Result_Click_3(object sender, EventArgs e)
    {
        LinkButton lb = (LinkButton)sender;

        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        hid3.Value = lb.Text;
        string containerId = "TabContent_Result_" + index.ToString();
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(lb.Text, lb.Text, "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result(lb.Text, lb.Text, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    protected void AspNetPager_Result_PageChanged_31(object src, EventArgs e)
    {
        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        BindGrid_Result(hid3.Value, hid3.Value, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    //安平區
    protected void TabButton_Result_Click_4(object sender, EventArgs e)
    {
        LinkButton lb = (LinkButton)sender;

        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        hid4.Value = lb.Text;
        string containerId = "TabContent_Result_" + index.ToString();
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(lb.Text, lb.Text, "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result(lb.Text, lb.Text, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    protected void AspNetPager_Result_PageChanged_41(object src, EventArgs e)
    {
        int index = 0;
        if (tc2.ActiveTabIndex.ToString() != "")
        {
            index = int.Parse(tc2.ActiveTabIndex.ToString()) - 1;
        }
        string GrirdViewId = "GVList_Result_" + index.ToString();
        string aspnetpageId = "AspNetPager_Result_" + index.ToString();

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        BindGrid_Result(hid4.Value, hid4.Value, aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    //安南區
    protected void TabButton_Result_Click_5(object sender, EventArgs e)
    {
        hid1.Value = "5";
        string containerId = "TabContent_Result_1";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_1";
        string aspnetpageId = "AspNetPager_Result_1";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;
        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(Dist[5], Dist[2], "");
        ApplyListInfo.Dispose_Result();
        //BindGrid(Dist[tc2.ActiveTabIndex], aspNetPager, gvlist);
        BindGrid_Result(Dist[5], Dist[2], aspNetPager, gvlist, "");


        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }
    //中西區
    protected void TabButton_Result_Click_6(object sender, EventArgs e)
    {
        hid1.Value = "6";
        string containerId = "TabContent_Result_1";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_1";
        string aspnetpageId = "AspNetPager_Result_1";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;
        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount(Dist[6], Dist[2], "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result(Dist[6], Dist[2], aspNetPager, gvlist, "");


        // 刻意暫停 2 秒
        Thread.Sleep(1000);
    }


    protected void TabButton_Result_Click_2_0(object sender, EventArgs e)
    {

        //Page.Header.Title = "TabContent_Result_1";
        int lb = int.Parse(((LinkButton)sender).ID.ToString().Split(new char[] { '_' })[1]);

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        hf.Value = lb.ToString();
        string containerId = "TabContent_Result_1";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_1";
        string aspnetpageId = "AspNetPager_Result_1";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }

    protected void TabButton_Result_Click_3_0(object sender, EventArgs e)
    {

        int lb = int.Parse(((LinkButton)sender).ID.ToString().Split(new char[] { '_' })[1]);

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        hf.Value = lb.ToString();
        string containerId = "TabContent_Result_3";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_3";
        string aspnetpageId = "AspNetPager_Result_3";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }

    protected void TabButton_Result_Click_4_0(object sender, EventArgs e)
    {

        int lb = int.Parse(((LinkButton)sender).ID.ToString().Split(new char[] { '_' })[1]);

        HiddenField hf = (HiddenField)(tc2.ActiveTab.FindControl("hid" + tc2.ActiveTabIndex));
        hf.Value = lb.ToString();
        string containerId = "TabContent_Result_4";
        Panel tabPanel = (Panel)(tc2.ActiveTab.FindControl(containerId));

        // 顯示某個索引標籤內的 Panel 控制項。
        if (tabPanel != null) tabPanel.Visible = true;

        string GrirdViewId = "GVList_Result_4";
        string aspnetpageId = "AspNetPager_Result_4";

        AspNetPager aspNetPager = (AspNetPager)(tc2.ActiveTab.FindControl(aspnetpageId));
        GridView gvlist = (GridView)(tc2.ActiveTab.FindControl(GrirdViewId));

        TNView_ApplyList ApplyListInfo = new TNView_ApplyList();

        gvlist.Visible = true;

        aspNetPager.RecordCount = ApplyListInfo.GetApplyResultCount("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", "");
        ApplyListInfo.Dispose_Result();
        BindGrid_Result("全部案件", "'東區','南區','北區','安平區','安南區','中西區'", aspNetPager, gvlist, "");
        // 刻意暫停 2 秒
        Thread.Sleep(1000);

    }
    protected void GridView1_RowDataBound(object sender, GridViewRowEventArgs e)
    {
        string newsid = "";
        if (e.Row.RowType == DataControlRowType.DataRow)
        {
            newsid = DataBinder.Eval(e.Row.DataItem, "NewsID").ToString();

            e.Row.Cells[1].Text = "<a href='javascript:opennews(" + newsid + ")'>" + DataBinder.Eval(e.Row.DataItem, "Topic").ToString() + "</a>";
        }
    }
}
